"""
A sample TCP Server which translates integer to binary, how it works:
    telnet localhost 2323
        byte?> 5
            0b101
        byte?> 9
            0b1001
"""

import asyncio
import sys

CRLF = b"\r\n"
PROMPT = b"byte?> "


async def handle_queries(reader, writer):
    while True:
        writer.write(PROMPT)
        await writer.drain()
        data = await reader.readline()
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = "\x00"
        client = writer.get_extra_info("peername")
        print("Received from {}: {!r}".format(client, query))
        if query:
            if ord(query[:1]) < 32:
                break
            try:
                byted = bytes(bin(int(query)), encoding="utf8")
                writer.write(byted + CRLF)
            except (ValueError, TypeError):
                writer.write(b"doesn't look like an integer :(" + CRLF)
                pass
            await writer.drain()
    print("Closed the client socket")
    writer.close()


def main(address="127.0.0.1", port=2323):
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(
        handle_queries, address, port, loop=loop
    )
    server = loop.run_until_complete(server_coro)
    host = server.sockets[0].getsockname()
    print("Serving on {}. Hit CTRL-C to stop.".format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
    print("Server shutting down.")
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main(*sys.argv[1:])
