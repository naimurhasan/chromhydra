(async () => {
  const echoUrl = __ECHO_URL__;
  const ipUrl = __IP_URL__;
  const workerSource = "postMessage({ua: navigator.userAgent, platform: navigator.platform, lang: navigator.language, tz: Intl.DateTimeFormat().resolvedOptions().timeZone, brands: navigator.userAgentData ? navigator.userAgentData.brands.map(b => b.brand) : []})";
  const worker = await new Promise(resolve => {
    try {
      const blob = new Blob([workerSource], {type: "application/javascript"});
      const instance = new Worker(URL.createObjectURL(blob));
      instance.onmessage = event => { resolve(event.data); instance.terminate(); };
      instance.onerror = () => resolve(null);
      setTimeout(() => resolve(null), 3000);
    } catch (error) {
      resolve(null);
    }
  });
  const getJson = async url => {
    if (!url) return null;
    try {
      return await (await fetch(url, {cache: "no-store"})).json();
    } catch (error) {
      return null;
    }
  };
  const lowerKeys = source => Object.fromEntries(Object.entries(source).map(([key, value]) => [key.toLowerCase(), value]));
  const echo = await getJson(echoUrl);
  const ip = await getJson(ipUrl);
  const uad = navigator.userAgentData;
  const high = uad ? await uad.getHighEntropyValues(["platformVersion", "architecture", "fullVersionList"]) : null;
  const gl = document.createElement("canvas").getContext("webgl");
  const debug = gl && gl.getExtension("WEBGL_debug_renderer_info");
  return JSON.stringify({
    ua: navigator.userAgent,
    platform: navigator.platform,
    webdriver: navigator.webdriver,
    brands: uad ? uad.brands.map(b => b.brand) : [],
    uadPlatform: uad ? uad.platform : "",
    platformVersion: high ? high.platformVersion : "",
    architecture: high ? high.architecture : "",
    fullVersionList: high ? high.fullVersionList.map(b => `${b.brand} ${b.version}`) : [],
    tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
    lang: navigator.language,
    languages: navigator.languages,
    worker,
    renderer: debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : "",
    headers: echo && echo.headers ? lowerKeys(echo.headers) : null,
    ip: ip ? {ip: ip.ip, timezone: ip.timezone, country: ip.country} : null
  });
})()
