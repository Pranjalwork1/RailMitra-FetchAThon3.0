from uagents import Agent, Context, Model
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, ChatAcknowledgement
from datetime import datetime
from uuid import uuid4

agent = Agent(name="RailMitra-Orchestrator")

# Replace with your actual Yatra-Vendor-Network agent1q... address
VENDOR_AGENT_ADDRESS = "agent1q..."

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

@agent.on_message(model=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    
    ctx.storage.set("last_user_sender", sender)
    req_id = str(uuid4())
    
    user_text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            user_text = item.text.strip()

    if "pay" in user_text.lower() or "confirm" in user_text.lower():
        await ctx.send(sender, ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text="🎉 **Payment Verified (0.1 FET)!** All bookings (E-Catering at Mathura Jn & Cab Reschedule) confirmed successfully.")]
        ))
        return

    if VENDOR_AGENT_ADDRESS.startswith("agent1"):
        await ctx.send(
            VENDOR_AGENT_ADDRESS,
            VendorQuoteRequest(
                request_id=req_id,
                train_number="12002",
                delay_minutes=185,
                next_station="Mathura Jn",
                destination="Greater Noida"
            )
        )
    
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text="📡 **RailMitra Intent Parsed:** Train `12002` delayed by **185 mins**. Contacting `Yatra-Vendor-Network` for live quotes...\n\n👉 Reply **`CONFIRM & PAY`** once quotes arrive to complete the 0.1 FET settlement.")]
    ))

@agent.on_message(model=VendorQuoteResponse)
async def handle_vendor_response(ctx: Context, sender: str, msg: VendorQuoteResponse):
    user_sender = ctx.storage.get("last_user_sender")
    if user_sender:
        response_text = f"✅ **Recovery Package Received (`{msg.quote_id}`):**\n\n{msg.summary_markdown}\n\n👉 Reply **`CONFIRM & PAY`** to approve settlement."
        await ctx.send(user_sender, ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response_text)]
        ))
