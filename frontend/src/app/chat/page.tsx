"use client";

import { useState } from "react";

import api from "@/lib/api";

export default function ChatPage() {

    const [question, setQuestion] =
        useState("");

    const [messages, setMessages] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(false);

    async function sendMessage() {

        if (!question.trim()) return;

        const userQuestion = question;

        setMessages(prev => [
            ...prev,
            {
                role: "user",
                content: userQuestion
            },
            {
                role: "assistant",
                content: ""
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
                        conversation_id: 1,
                        question: userQuestion
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
                        result.value || new Uint8Array()
                    );

                streamedText += chunk;

                setMessages(prev => {

                    const updated = [...prev];

                    updated[
                        updated.length - 1
                    ] = {
                        role: "assistant",
                        content: streamedText
                    };

                    return updated;
                });
            }

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    }

    return (

        <div className="flex flex-col h-screen bg-black text-white p-6">

            {/* Header */}
            <h1 className="text-3xl font-bold mb-6">
                ODIN Chat
            </h1>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto border border-gray-800 rounded-xl p-4">

                {messages.map((msg, index) => (

                    <div
                        key={index}
                        className={`mb-4 flex ${msg.role === "user"
                                ? "justify-end"
                                : "justify-start"
                            }`}
                    >

                        <div
                            className={`inline-block rounded-lg px-4 py-2 max-w-[70%] ${msg.role === "user"
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

                        </div>

                    </div>

                ))}

                {/* Loading Indicator */}
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
                        setQuestion(e.target.value)
                    }

                    onKeyDown={(e) => {

                        if (e.key === "Enter") {
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
    );
}