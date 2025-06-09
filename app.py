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

if session == "":
	session = "telethon"
else:
	session = os.path.join(config.sessions, session)
	
client = TelegramClient(
	session,
	config.API_ID,
	config.API_HASH,
	system_version="5.9"
)

filters = [
	{
		"title": "Новые",
		"exclude_peers": [],
		"contacts": True,
		"non_contacts": True,
		"groups": True,
		"broadcasts": True,
		"bots": True,
		"exclude_muted": True,
		"exclude_read": True,
		"emoticon": "✅"
	},
	{
		"title": "Контакты",
		"exclude_peers": [],
		"contacts": True,
		"non_contacts": True,
		"emoticon": "👤"
	},
	{
		"title": "Группы",
		"exclude_peers": [],
		"groups": True,
		"emoticon": "👥"
	},
	{
		"title": "Каналы",
		"exclude_peers": [],
		"broadcasts": True,
		"emoticon": "📢"
	},
	{
		"title": "Боты",
		"exclude_peers": [],
		"bots": True,
		"emoticon": "🤖"
	}
]

async def main():
	me = await client.get_input_entity("me")

	for id, filter_kwargs in enumerate(filters, 2):
		title = filter_kwargs["title"]

		filter = types.DialogFilter(
			id=id,
			pinned_peers=[me],
			include_peers=[me],
			**filter_kwargs
		)

		try:
			await client(functions.messages.UpdateDialogFilterRequest(
				id=id,
				filter=filter
			))
		except TypeError as error:
			if error.args[0] == "a TLObject was expected but found something else":
				filter_kwargs["title"] = types.TextWithEntities(filter_kwargs["title"], [])

				filter = types.DialogFilter(
					id=id,
					pinned_peers=[me],
					include_peers=[me],
					**filter_kwargs
				)

				await client(functions.messages.UpdateDialogFilterRequest(
					id=id,
					filter=filter
				))
			else:
				raise

		console.log(f"Created folder [bold]{title}[/bold] with ID [bold]{id}[/bold]")

	await client(functions.messages.UpdateDialogFiltersOrderRequest(
		order=[i + 2 for i in range(len(filters))]
	))

	console.log(f"Ordered folders")

with client:
	client.loop.run_until_complete(main())
