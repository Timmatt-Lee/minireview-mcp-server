#!/bin/bash

# Activate venv if it exists
[ -f .venv/bin/activate ] && source .venv/bin/activate

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting ADK API server in the background..."
# Start the server and send its output to a log file
adk api_server . > adk_server.log 2>&1 &
SERVER_PID=$!

# Cleanup function
cleanup() {
    echo "Cleaning up and stopping ADK server (PID: $SERVER_PID)..."
    # Check if the process exists before trying to kill it
    if ps -p $SERVER_PID > /dev/null; then
        kill $SERVER_PID
    fi
    rm -f adk_server.log
}
trap cleanup EXIT

# Wait for the server to start
echo "Waiting for server to become available..."
TIMEOUT=15
ELAPSED=0
until curl -s -f http://localhost:8000/list-apps > /dev/null; do
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "Error: Server did not start within $TIMEOUT seconds."
        echo "--- Server Log (adk_server.log) ---"
        cat adk_server.log
        exit 1
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

echo "Server is up. Step 1: Creating session..."

# Step 1: Create a session
SESSION_RESPONSE=$(curl -s -X POST http://localhost:8000/apps/minireview_agent/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"state": {"key1": "value1", "key2": 42}}')

# Check if session creation was successful
if echo "$SESSION_RESPONSE" | grep -q '"minireview_agent"'; then
    echo "Session created successfully."
else
    echo "Error: Failed to create session."
    echo "Response: $SESSION_RESPONSE"
    echo "--- Server Log (adk_server.log) ---"
    cat adk_server.log
    exit 1
fi

echo "Step 2: Running query..."

# # Step 2: Run a query
# RUN_RESPONSE=$(curl -s -X POST http://localhost:8000/run \
# -H "Content-Type: application/json" \
# -d '{
# "app_name": "minireview_agent",
# "user_id": "u_123",
# "session_id": "s_123",
# "new_message": {
#     "role": "user",
#     "parts": [{
#     "text": "so what can you do"
#     }]
# }
# }')

# # Check if the run was successful
# if echo "$RUN_RESPONSE" | grep -q '"content"'; then
#     echo "Success: Agent responded correctly."
#     exit 0
# else
#     echo "Error: Agent did not respond as expected."
#     echo "Response: $RUN_RESPONSE"
#     echo "--- Server Log (adk_server.log) ---"
#     cat adk_server.log
#     exit 1
# fi
