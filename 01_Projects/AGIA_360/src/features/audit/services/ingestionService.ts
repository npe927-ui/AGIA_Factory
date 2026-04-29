import { supabase } from '@/shared/lib/supabase';
import { generateEmbeddings } from '@/shared/lib/ai'; // We'll create this next

export interface IngestionOptions {
    chunkSize?: number;
    chunkOverlap?: number;
}

export async function ingestDocument(title: string, content: string, source: string, options: IngestionOptions = {}) {
    const { chunkSize = 1000, chunkOverlap = 200 } = options;

    console.log(`Ingesting document: ${title}`);

    // 1. Create document entry
    const { data: doc, error: docError } = await supabase
        .from('documents')
        .insert({ title, source })
        .select()
        .single();

    if (docError) throw docError;

    // 2. Simple chunking
    const chunks = chunkText(content, chunkSize, chunkOverlap);
    console.log(`Created ${chunks.length} chunks`);

    // 3. Process chunks in batches (to avoid rate limits/timeouts)
    const batchSize = 10;
    for (let i = 0; i < chunks.length; i += batchSize) {
        const batch = chunks.slice(i, i + batchSize);
        console.log(`Processing batch ${Math.floor(i / batchSize) + 1} of ${Math.ceil(chunks.length / batchSize)}`);

        const embeddings = await generateEmbeddings(batch);

        const chunkInserts = batch.map((text, index) => ({
            document_id: doc.id,
            content: text,
            embedding: embeddings[index],
            metadata: { index: i + index, title }
        }));

        const { error: chunkError } = await supabase
            .from('chunks')
            .insert(chunkInserts);

        if (chunkError) throw chunkError;
    }

    return doc;
}

export async function searchChunks(query: string, matchCount: number = 5) {
    return searchAgiaCorpus(query, matchCount);
}

export async function searchAgiaCorpus(query: string, matchCount: number = 5) {
    const [embedding] = await generateEmbeddings([query]);

    const { data, error } = await supabase.rpc('match_agia_corpus', {
        query_embedding: embedding,
        match_threshold: 0.5,
        match_count: matchCount
    });

    if (error) {
        console.error('Error in match_agia_corpus:', error);
        throw error;
    }
    return data;
}

function chunkText(text: string, size: number, overlap: number): string[] {
    const chunks: string[] = [];
    let start = 0;

    while (start < text.length) {
        const end = Math.min(start + size, text.length);
        chunks.push(text.slice(start, end));
        start += size - overlap;
    }

    return chunks;
}
