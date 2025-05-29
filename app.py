import asyncio
import os
import re
import sys

from telethon import errors, functions, TelegramClient
from telethon.tl import types

from rich.console import Console

import config

console = Console(highlight=False)

if len(sys.argv) == 1:
	session = console.input(f"Session (in [bold]{config.sessions}[/bold]): ")
else:
	session = " ".join(sys.argv[1:])

client = TelegramClient(
	os.path.join(config.sessions, session),
	config.API_ID,
	config.API_HASH,
	system_version="5.9"
)

async def main():
	await client(functions.messages.UpdateDialogFilterRequest(
		id=2,
        filter=types.DialogFilter(
            id=2,
            title=types.TextWithEntities("Новые", []),
            pinned_peers=[await client.get_input_entity("me")],
            include_peers=[await client.get_input_entity("me")],
            exclude_peers=[],
            contacts=True,
            non_contacts=True,
            groups=True,
            broadcasts=True,
            bots=True,
			exclude_muted=True,
			exclude_read=True,
			emoticon="✅"
        )
	))
	
	await client(functions.messages.UpdateDialogFilterRequest(
		id=3,
        filter=types.DialogFilter(
            id=3,
            title=types.TextWithEntities("Контакты", []),
            pinned_peers=[await client.get_input_entity("me")],
            include_peers=[await client.get_input_entity("me")],
            exclude_peers=[],
            contacts=True,
            non_contacts=True,
			emoticon="👤"
        )
	))
	
	await client(functions.messages.UpdateDialogFilterRequest(
		id=4,
        filter=types.DialogFilter(
            id=4,
            title=types.TextWithEntities("Группы", []),
            pinned_peers=[await client.get_input_entity("me")],
            include_peers=[await client.get_input_entity("me")],
            exclude_peers=[],
            groups=True,
			emoticon="👥"
        )
	))
	
	await client(functions.messages.UpdateDialogFilterRequest(
		id=5,
        filter=types.DialogFilter(
            id=5,
            title=types.TextWithEntities("Каналы", []),
            pinned_peers=[await client.get_input_entity("me")],
            include_peers=[await client.get_input_entity("me")],
            exclude_peers=[],
            broadcasts=True,
			emoticon="📢"
        )
	))
	
	await client(functions.messages.UpdateDialogFilterRequest(
		id=6,
        filter=types.DialogFilter(
            id=6,
            title=types.TextWithEntities("Боты", []),
            pinned_peers=[await client.get_input_entity("me")],
            include_peers=[await client.get_input_entity("me")],
            exclude_peers=[],
            bots=True,
			emoticon="🤖"
        )
	))

with client:
	client.loop.run_until_complete(main())