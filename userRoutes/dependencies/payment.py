from fastapi import HTTPException

async def process_payment(payment_method: str, card_details: dict, amount: float):
    if payment_method.lower() in ["credit_card", "debit_card", "stripe"]:
        if not card_details or not validate_card_details(card_details):
            raise HTTPException(
                status_code=400,
                detail="Invalid or missing card details."
            )
        # mock payment gateway rn.
        payment_successful = mock_payment_gateway(card_details, amount)
        if not payment_successful:
            raise HTTPException(
                status_code=402,
                detail="Payment processing failed."
            )
        return "COMPLETED"  
    elif payment_method.lower() == "cash_on_delivery":
        return "PENDING"  
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported payment method."
        )

def validate_card_details(card_details: dict) -> bool:
    return all(key in card_details for key in ["card_number", "expiry_date", "cvv"])

def mock_payment_gateway(card_details: dict, amount: float) -> bool:
    # Simulate a payment gateway. have to implement real integration.
    return True
