def wallet_balance(request):
    if request.user.is_authenticated:
        try:
            return {"wallet_balance": request.user.wallet.balance}
        except:
            return {"wallet_balance": 0}
    return {"wallet_balance": None}