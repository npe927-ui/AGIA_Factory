'use client';

import { useState, useRef, useEffect } from 'react';
import type { Message, AgentType } from '../services/managerService';

interface ChatMessage extends Message {
    agent?: AgentType;
}

const AGENT_LABELS: Record<AgentType, string> = {
    MANAGER: '🌙 Lua — Manager',

    CLOSER: '🎯 Closer Agent',
    EMKD: '📧 Email Agent',
    CONTENT: '📱 Content Agent',
};

const AGENT_COLORS: Record<AgentType, string> = {
    MANAGER: 'bg-indigo-500',

    CLOSER: 'bg-green-500',
    EMKD: 'bg-orange-500',
    CONTENT: 'bg-pink-500',
};

export function ManagerChat() {
    const [messages, setMessages] = useState<ChatMessage[]>([
        {
            role: 'assistant',
            content: '¡Hola! Soy Lua, la Manager Agent de Agia 360. Como la luna guía a los navegantes, yo guío tu negocio a través de la IA y las ventas. Estoy entrenada con las mejores metodologías del mundo: SPIN, Challenger Sale, Cialdini, Sandler y más. ¿Por dónde empezamos?',
            agent: 'MANAGER',
        },
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async () => {
        const trimmed = input.trim();
        if (!trimmed || isLoading) return;

        const userMessage: ChatMessage = { role: 'user', content: trimmed };
        const updatedMessages = [...messages, userMessage];
        setMessages(updatedMessages);
        setInput('');
        setIsLoading(true);

        try {
            const history: Message[] = updatedMessages
                .filter((m) => m.role === 'user' || m.role === 'assistant')
                .map(({ role, content }) => ({ role, content }));

            const res = await fetch('/api/manager', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: trimmed, history: history.slice(0, -1) }),
            });

            if (!res.ok) throw new Error('API error');

            const data = await res.json();

            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: data.response,
                    agent: data.agent as AgentType,
                },
            ]);
        } catch {
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: 'Lo siento, hubo un error. Por favor, inténtalo de nuevo.',
                    agent: 'MANAGER',
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-8rem)] max-w-4xl mx-auto">
            {/* Header */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-t-2xl p-6 text-white">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
                        🌙
                    </div>
                    <div>
                        <h2 className="font-bold text-xl">Lua — Manager Agent</h2>
                        <p className="text-white/70 text-sm">Coordinadora 360 · Agia 360</p>
                    </div>
                    <div className="ml-auto flex items-center gap-2">
                        <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span className="text-sm text-white/70">En línea</span>
                    </div>
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto bg-gray-50 p-6 space-y-4">
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div className={`max-w-[75%] ${msg.role === 'user' ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
                            {msg.role === 'assistant' && msg.agent && (
                                <div className="flex items-center gap-2">
                                    <span className={`text-xs text-white px-2 py-0.5 rounded-full ${AGENT_COLORS[msg.agent]}`}>
                                        {AGENT_LABELS[msg.agent]}
                                    </span>
                                </div>
                            )}
                            <div
                                className={`rounded-2xl px-5 py-3 text-sm leading-relaxed whitespace-pre-wrap ${msg.role === 'user'
                                    ? 'bg-indigo-600 text-white rounded-tr-sm'
                                    : 'bg-white text-gray-800 shadow-sm border border-gray-100 rounded-tl-sm'
                                    }`}
                            >
                                {msg.content}
                            </div>
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white rounded-2xl rounded-tl-sm px-5 py-3 shadow-sm border border-gray-100">
                            <div className="flex gap-1.5">
                                <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={bottomRef} />
            </div>

            {/* Input */}
            <div className="bg-white border-t border-gray-200 rounded-b-2xl p-4">
                <div className="flex gap-3">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Escribe tu pregunta... (Enter para enviar)"
                        rows={2}
                        className="flex-1 resize-none rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                    <button
                        onClick={sendMessage}
                        disabled={!input.trim() || isLoading}
                        className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl px-5 py-3 font-semibold transition-colors"
                    >
                        Enviar
                    </button>
                </div>
                <p className="text-xs text-gray-400 mt-2 text-center">
                    Respaldado por Claude Sonnet · Dataset Premium Activo ✓ · SPIN · Challenger · Cialdini · Sandler
                </p>
            </div>
        </div>
    );
}
