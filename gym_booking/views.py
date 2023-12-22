from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
# gym_booking/views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, GymMembership, Payment
from .paystack import Paystack
from .serializers import \
    PaymentSerializer  # Create this serializer if not already done
from .serializers import (GymMembershipSerializer, UserLoginSerializer,
                          UserRegistrationSerializer)
from .utils import generate_user_id  # Import the function

# views.py


# views.py



class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Override the user_id with a 4-digit value
        # serializer.validated_data['user_id'] = generate_user_id()

        # Call the create method on the serializer
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED, headers=headers)

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Print or log debugging information
        print(f"Login attempt with data: {request.data}")

        user = serializer.validated_data["user"]
        login(request, user)
        return Response({'detail': 'User logged in successfully.'}, status=status.HTTP_200_OK)

class GymMembershipViewSet(viewsets.ModelViewSet):
    queryset = GymMembership.objects.all()
    serializer_class = GymMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current_user_membership(self, request):
        user_membership = get_object_or_404(GymMembership, user=request.user)
        serializer = self.get_serializer(user_membership)
        return Response(serializer.data)

    # Add other actions and overrides as needed

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def verify(self, request, pk):
        payment = self.get_object()
        paystack = Paystack()
        status, result = paystack.verify_payment(payment.ref, payment.amount)

        if status:
            # Process the payment verification result...
            return Response({'detail': 'Payment verified successfully'}, status=status.HTTP_200_OK)
        else:
            # Handle verification failure...
            return Response({'detail': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)

    # Add other actions and overrides as needed



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gym_payment_api(request):
    try:
        user_membership, created = GymMembership.objects.get_or_create(user=request.user)

        amount = request.data.get('amount')
        email = request.user.email
        new_plan = request.data.get('plan')

        payment = Payment.objects.create(amount=amount, email=email, user=request.user, plan=new_plan)
        payment.save()

        active_subscription = Subscription.objects.filter(user=request.user, expiry_date__gt=timezone.now()).first()

        if active_subscription and not active_subscription.is_active():
            # Change the plan immediately if the previous plan is inactive
            set_membership_plan(user_membership, new_plan)
            active_subscription.delete()  # Remove the inactive subscription
        else:
            # Create a new subscription with the initial expiry date based on the new plan
            expiry_days = get_expiry_days_for_plan(new_plan)
            new_subscription = Subscription.objects.create(
                user=request.user,
                plan=new_plan,
                expiry_date=timezone.now() + timezone.timedelta(days=expiry_days)
            )

        serializer = PaymentSerializer(payment)

        context = {
            'payment': serializer.data,
            'field_values': request.data,
            'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
            'amount_value': payment.amount_value(),
        }
        return Response(context, status=status.HTTP_201_CREATED)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_gym_api(request, ref):
    try:
        payment = Payment.objects.get(ref=ref)
        verified = payment.verify_payment()

        user_membership, created = GymMembership.objects.get_or_create(user=request.user)

        if verified:
            new_plan = get_plan_for_amount(payment.amount)  # Assuming you have a function to map amount to a plan
            user_membership.set_membership_plan(new_plan)
            print(request.user.username, " Membership registration successfully")
            return Response({'message': 'Membership registration successful'}, status=status.HTTP_200_OK)

        return Response({'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)

    except Payment.DoesNotExist:
        return Response({'message': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    except GymMembership.DoesNotExist:
        return Response({'message': 'Gym membership not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GymDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve the user's gym membership
            user_membership = GymMembership.objects.get(user=request.user)
            user_membership.set_plan_status()
            payment_history = Payment.objects.filter(user=request.user)

            context = {
                'user_membership': {
                    'user_id': request.user.user_id,
                    'plan': user_membership.plan,
                    'plan_status': user_membership.plan_status,
                },
                'payment_history': [
                    {
                        'amount': payment.amount,
                        'verified': payment.verified,
                        'ref': payment.ref,
                        'date_created': payment.date_created,
                    }
                    for payment in payment_history
                ],
            }

            return Response(context)

        except GymMembership.DoesNotExist:
            return Response({'error_message': 'Gym membership not found.'}, status=404)