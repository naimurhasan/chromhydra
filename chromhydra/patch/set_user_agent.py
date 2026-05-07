import mycdp as cdp

from chromhydra.hints.client_hints import client_hints
from chromhydra.hints.host_info import host_info
from chromhydra.patch.to_cdp_metadata import to_cdp_metadata


async def set_user_agent(self, user_agent="", accept_language=None, platform=None):
    _, product, _, default_agent, _ = await self.send(cdp.browser.get_version())
    agent = user_agent or default_agent.replace("HeadlessChrome", "Chrome")
    hints = client_hints(agent, product.split("/")[-1], host_info())
    await self.send(
        cdp.network.set_user_agent_override(
            user_agent=agent,
            accept_language=accept_language,
            platform=platform,
            user_agent_metadata=to_cdp_metadata(hints),
        )
    )
