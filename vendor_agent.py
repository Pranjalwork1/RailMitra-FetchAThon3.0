from uagents import Agent, Context, Model

agent = Agent(name="yatra_vendor_network")

class VendorQuoteRequest(Model):
    request_id: str
    train_number: str
    delay_minutes: int
    next_station: str
    destination: str

class VendorQuoteResponse(Model):
    request_id: str
    quote_id: str
    summary_markdown: str

@agent.on_message(model=VendorQuoteRequest)
async def handle_vendor_request(
    ctx: Context,
    sender: str,
    msg: VendorQuoteRequest,
):
    ctx.logger.info(f"QUOTE_REQUEST_RECEIVED train={msg.train_number} request_id={msg.request_id}")
    
    quote_id = f"YATRA-{msg.request_id[:8].upper()}"

    summary = (
        f"### RailMitra Recovery Proposal: {quote_id}\n\n"
        f"- **Train:** {msg.train_number}\n"
        f"- **Delay:** {msg.delay_minutes} minutes\n"
        f"- **E-Catering:** Proposed meal at {msg.next_station}\n"
        f"- **Cab:** Proposed rescheduling for {msg.destination}\n"
        f"- **Settlement:** Proposed fee of 0.1 FET, subject to explicit approval and payment verification.\n\n"
        "These are proposed services, not confirmed bookings."
    )

    await ctx.send(
        sender,
        VendorQuoteResponse(
            request_id=msg.request_id,
            quote_id=quote_id,
            summary_markdown=summary,
        ),
    )

    ctx.logger.info(f"QUOTE_RESPONSE_SENT request_id={msg.request_id}")

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"YATRA_READY address={ctx.agent.address}")
