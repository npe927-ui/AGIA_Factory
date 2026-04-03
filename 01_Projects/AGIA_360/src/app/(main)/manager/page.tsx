import { ManagerChat } from '@/features/manager/components/ManagerChat';

export default function ManagerPage() {
    return (
        <div className="p-6">
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Manager Agent</h1>
                <p className="text-gray-500 mt-1">
                    Tu coordinador central de IA · Powered by Claude Sonnet + Dataset Premium
                </p>
            </div>
            <ManagerChat />
        </div>
    );
}
