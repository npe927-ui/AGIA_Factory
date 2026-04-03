import { NextRequest, NextResponse } from 'next/server';
import { ingestDocument } from '@/features/audit/services/ingestionService';

export const maxDuration = 60; // Aumentar a 60s para ingestas grandes

export async function POST(req: NextRequest) {
    try {
        const body = await req.json();
        const { title, content, source } = body;

        if (!title || !content) {
            return NextResponse.json({ error: 'title and content are required' }, { status: 400 });
        }

        const doc = await ingestDocument(title, content, source || 'notebooklm', {
            chunkSize: 800,
            chunkOverlap: 150,
        });

        return NextResponse.json({ success: true, documentId: doc.id, title: doc.title });
    } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown error';
        console.error('[ingest] Error:', message);
        return NextResponse.json({ error: message }, { status: 500 });
    }
}
