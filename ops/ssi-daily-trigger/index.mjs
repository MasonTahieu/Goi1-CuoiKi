const snapshotUrl = "https://cuoiki.vercel.app/api/snapshot?source=daily";
const dispatchUrl = "https://api.github.com/repos/MasonTahieu/Goi1-CuoiKi/actions/workflows/ssi-daily.yml/dispatches";

export async function triggerDaily(scheduledTime, token, request = fetch) {
  if (!token) throw new Error("Missing GitHub workflow token");
  const date = new Intl.DateTimeFormat("sv-SE", { timeZone: "Asia/Ho_Chi_Minh", dateStyle: "short" })
    .format(scheduledTime);

  // If the dashboard check fails, still let the workflow try to catch up.
  let snapshot;
  try {
    const response = await request(snapshotUrl, { signal: AbortSignal.timeout(8000) });
    if (response.ok) snapshot = await response.json();
  } catch {
    console.warn("Dashboard check did not finish. Dispatching the daily workflow.");
  }
  if (snapshot?.as_of?.slice(0, 10) === date && snapshot.groups?.VN30?.ranked === 30) {
    return { date, status: "already_published" };
  }

  const response = await request(dispatchUrl, {
    method: "POST",
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "cuoiki-ssi-daily-trigger",
      "X-GitHub-Api-Version": "2026-03-10",
    },
    body: JSON.stringify({ ref: "main" }),
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) throw new Error(`GitHub dispatch returned HTTP ${response.status}`);
  return { date, status: "dispatched" };
}

export default {
  async scheduled(controller, env) {
    console.log(await triggerDaily(controller.scheduledTime, env.GITHUB_ACTIONS_TOKEN));
  },
};
