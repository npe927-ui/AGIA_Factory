import { NextRequest, NextResponse } from 'next/server';
import { processWithManager, Message } from '@/features/manager/services/managerService';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { message, history = [] }: { message: string; history: Message[] } = body;

        if (!message?.trim()) {
            return NextResponse.json({ error: 'Message is required' }, { status: 400 });
        }

        const result = await processWithManager(message, history);
        return NextResponse.json(result);
    } catch (error) {
        console.error('Manager API error:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
}
