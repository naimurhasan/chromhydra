import mycdp as cdp


def to_cdp_metadata(hints: dict) -> cdp.emulation.UserAgentMetadata:
    brand = cdp.emulation.UserAgentBrandVersion
    return cdp.emulation.UserAgentMetadata(
        platform=hints["platform"],
        platform_version=hints["platform_version"],
        architecture=hints["architecture"],
        model=hints["model"],
        mobile=hints["mobile"],
        brands=[brand(b["brand"], b["version"]) for b in hints["brands"]],
        full_version_list=[brand(b["brand"], b["version"]) for b in hints["full_version_list"]],
        full_version=hints["full_version"],
        bitness=hints["bitness"],
        wow64=hints["wow64"],
    )
