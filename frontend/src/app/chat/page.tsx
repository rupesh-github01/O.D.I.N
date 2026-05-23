"use client";

import {
  useEffect,
  useState
} from "react";

export default function ChatPage() {

  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState<any[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [
    conversationId,
    setConversationId
  ] = useState<number | null>(null);

  const [
    conversations,
    setConversations
  ] = useState<any[]>([]);

  // Fetch conversations
  async function fetchConversations() {

    try {

      const response = await fetch(
        "http://localhost:8000/conversations"
      );

      const data =
        await response.json();

      setConversations(data);

      if (
        data.length > 0 &&
        !conversationId
      ) {

        setConversationId(
          data[0].id
        );

      }

    } catch (error) {

      console.error(error);

    }
  }

  // Create new conversation
  async function createConversation() {

    try {

      const response = await fetch(
        "http://localhost:8000/conversations",
        {
          method: "POST"
        }
      );

      const data =
        await response.json();

      await fetchConversations();

      setConversationId(
        data.conversation_id
      );

      setMessages([]);

    } catch (error) {

      console.error(error);

    }
  }

  // Load conversations initially
  useEffect(() => {

    fetchConversations();

  }, []);

  // Send message
  async function sendMessage() {

    if (
      !question.trim() ||
      !conversationId
    ) return;

    const userQuestion = question;

    // Add user message immediately
    setMessages(prev => [
      ...prev,

      {
        role: "user",
        content: userQuestion
      },

      {
        role: "assistant",
        content: "",
        citations: []
      }
    ]);

    setQuestion("");

    setLoading(true);

    try {

      const response = await fetch(
        "http://localhost:8000/chat/stream",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            conversation_id:
              conversationId,

            question:
              userQuestion
          })
        }
      );

      if (!response.body) return;

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let done = false;

      let streamedText = "";

      while (!done) {

        const result =
          await reader.read();

        done = result.done;

        const chunk =
          decoder.decode(
            result.value ||
            new Uint8Array()
          );

        streamedText += chunk;

        setMessages(prev => {

          const updated = [...prev];

          updated[
            updated.length - 1
          ] = {
            role: "assistant",
            content: streamedText,
            citations: []
          };

          return updated;
        });
      }

    } catch (error) {

      console.error(error);

      alert(
        "Failed to contact ODIN backend."
      );

    } finally {

      setLoading(false);

    }
  }

  return (

    <div className="flex h-screen bg-black text-white">

      {/* Sidebar */}
      <div className="w-72 border-r border-gray-800 p-4 flex flex-col">

        <h1 className="text-2xl font-bold mb-6">
          ODIN
        </h1>

        <button
          onClick={createConversation}
          className="bg-blue-600 hover:bg-blue-700 rounded-lg px-4 py-2 mb-4"
        >

          + New Chat

        </button>

        <div className="flex-1 overflow-y-auto">

          {conversations.map((conv) => (

            <div
              key={conv.id}

              onClick={() =>
                setConversationId(
                  conv.id
                )
              }

              className={`p-3 rounded-lg cursor-pointer mb-2 transition-colors ${
                conversationId === conv.id
                  ? "bg-gray-800"
                  : "bg-gray-900 hover:bg-gray-800"
              }`}
            >

              Conversation {conv.id}

            </div>

          ))}

        </div>

      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col p-6">

        {/* Header */}
        <h1 className="text-3xl font-bold mb-6">

          ODIN Chat

        </h1>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto border border-gray-800 rounded-xl p-4">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={`mb-4 flex ${
                msg.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >

              <div
                className={`inline-block rounded-lg px-4 py-2 max-w-[70%] ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-white"
                }`}
              >

                <strong className="block mb-1 capitalize">

                  {msg.role}

                </strong>

                <p className="whitespace-pre-wrap">

                  {msg.content}

                </p>

                {/* Citations */}
                {msg.citations &&
                 msg.citations.length > 0 && (

                  <div className="mt-3 text-sm text-gray-400">

                    <p className="font-semibold mb-1">
                      Sources:
                    </p>

                    {msg.citations.map(
                      (
                        citation: any,
                        idx: number
                      ) => (

                        <div key={idx}>

                          • {citation.source}
                          {" "}
                          (
                          {citation.score.toFixed(2)}
                          )

                        </div>

                      )
                    )}

                  </div>

                )}

              </div>

            </div>

          ))}

          {/* Loading */}
          {loading && (

            <div className="mb-4 flex justify-start">

              <div className="bg-gray-800 text-white rounded-lg px-4 py-2 animate-pulse">

                ODIN is thinking...

              </div>

            </div>

          )}

        </div>

        {/* Input Area */}
        <div className="mt-4 flex gap-2">

          <input
            className="flex-1 border border-gray-700 bg-gray-900 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"

            value={question}

            onChange={(e) =>
              setQuestion(
                e.target.value
              )
            }

            onKeyDown={(e) => {

              if (
                e.key === "Enter" &&
                !loading
              ) {

                sendMessage();

              }

            }}

            placeholder="Ask ODIN..."

            disabled={loading}
          />

          <button
            className="bg-blue-600 hover:bg-blue-700 transition-colors text-white px-6 py-2 rounded-lg disabled:opacity-50"

            onClick={sendMessage}

            disabled={loading}
          >

            {loading
              ? "Thinking..."
              : "Send"}

          </button>

        </div>

      </div>

    </div>
  );
}