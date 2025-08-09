# mgame/utils.py
from decimal import Decimal
from .models import Wallet, Transaction

def credit_wallet(user, amount, description="Top-up"):
    try:
        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.balance += Decimal(str(amount))
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=Decimal(str(amount)),
            type='credit',
            description=description
        )
    except Exception as e:
        print("❌ Wallet credit error:", e)

def debit_wallet(user, amount, description="Game fee"):
    try:
        wallet = Wallet.objects.get(user=user)
        if wallet.balance >= Decimal(str(amount)):
            wallet.balance -= Decimal(str(amount))
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=Decimal(str(amount)),
                type='debit',
                description=description
            )
            return True
        else:
            print("[!] Insufficient balance for:", user.username)
            return False
    except Wallet.DoesNotExist:
        print("[!] Wallet not found for user:", user.username)
        return False
