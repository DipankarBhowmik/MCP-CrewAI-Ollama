const { spawn } = require("child_process");
const readline = require("readline");

// Start Python MCP server
const pythonProcess = spawn("python", ["math_mcp_server.py"]);

// Read only stdout (clean JSON)
const rl = readline.createInterface({
  input: pythonProcess.stdout,
});

// ---------- Helpers ----------

function sendRequest(method, params = {}) {
  const request = {
    jsonrpc: "2.0",
    id: Date.now(),
    method,
    params,
  };

  pythonProcess.stdin.write(JSON.stringify(request) + "\n");
}

function sendNotification(method, params = {}) {
  const request = {
    jsonrpc: "2.0",
    method,
    params,
  };

  pythonProcess.stdin.write(JSON.stringify(request) + "\n");
}

// ---------- Clean Output ----------

rl.on("line", (line) => {
  try {
    const res = JSON.parse(line);

    // Only print final results
    if (res.result?.structuredContent?.result !== undefined) {
      console.log("✅ Result:", res.result.structuredContent.result);
    }

  } catch {
    // ignore non-JSON logs
  }
});

// ❌ Ignore noisy stderr logs completely
pythonProcess.stderr.on("data", () => {});

// ---------- MCP Flow ----------

setTimeout(() => {
  sendRequest("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: {
      name: "node-client",
      version: "1.0.0",
    },
  });
}, 200);

setTimeout(() => {
  // ✅ FIXED notification name
  sendNotification("notifications/initialized", {});
}, 400);

setTimeout(() => {
  sendRequest("tools/list", {});
}, 600);

setTimeout(() => {
  sendRequest("tools/call", {
    name: "add",
    arguments: { a: 10, b: 5 },
  });

  sendRequest("tools/call", {
    name: "multiply",
    arguments: { a: 6, b: 7 },
  });
}, 800);