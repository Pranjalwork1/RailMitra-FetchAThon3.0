
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    EndSessionContent,
    chat_protocol_spec,
)

agent = Agent()

chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(ChatMessage)
async def handle_chat(
    ctx: Context,
    sender: str,
    msg: ChatMessage,
):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            acknowledged_msg_id=msg.msg_id
        ),
    )

    text = msg.text()

    await ctx.send(
        sender,
        ChatMessage(
            content=[
                TextContent(
                    type="text",
                    text=(
                        "RailMitra-Orchestrator is online. "
                        f"I received: {text}"
                    ),
                ),
                EndSessionContent(type="end-session"),
            ],
        ),
    )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(
    ctx: Context,
    sender: str,
    msg: ChatAcknowledgement,
):
    ctx.logger.info("Chat acknowledgement received")


# Diagnostic: identify missing protocol handlers before
# Agentverse attempts to register the protocol.

models = set(chat_proto.models.keys())

handlers = (
    set(chat_proto.signed_message_handlers.keys())
    | set(chat_proto.unsigned_message_handlers.keys())
)

missing = models - handlers

print("CHAT_PROTOCOL_MODELS:", len(models))
print("CHAT_PROTOCOL_HANDLERS:", len(handlers))
print("CHAT_PROTOCOL_MISSING:", missing)

agent.include(chat_proto, publish_manifest=True)
