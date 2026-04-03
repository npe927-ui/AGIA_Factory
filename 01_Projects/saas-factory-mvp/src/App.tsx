import React from 'react';
import { supabase } from './lib/supabase';

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white selection:bg-emerald-500/30">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-slate-950/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center font-bold text-slate-950">SF</div>
            <span className="font-bold text-xl tracking-tight">SaaS Factory MVP</span>
          </div>
          <div className="flex items-center gap-6 text-sm font-medium text-slate-400">
            <a href="#" className="hover:text-white transition-colors">Docs</a>
            <a href="#" className="hover:text-white transition-colors">GitHub</a>
            <button className="px-4 py-2 rounded-full bg-white text-slate-950 hover:bg-slate-200 transition-colors">
              Deploy Now
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/20 bg-emerald-500/10 text-emerald-400 text-xs font-semibold mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            Ready for Production
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 bg-gradient-to-b from-white to-slate-400 bg-clip-text text-transparent">
            Build your SaaS at <br />
            <span className="text-emerald-500">Industrial Speed</span>
          </h1>
          <p className="text-lg text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed">
            The precision of a factory, the agility of a startup. Our industrial-grade boilerplate includes authentication, database, and CI/CD ready for deployment.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button className="w-full sm:w-auto px-8 py-4 rounded-xl bg-emerald-500 text-slate-950 font-bold hover:bg-emerald-400 transform hover:-translate-y-0.5 transition-all shadow-lg shadow-emerald-500/20">
              Launch Terminal
            </button>
            <button className="w-full sm:w-auto px-8 py-4 rounded-xl border border-white/10 bg-white/5 font-semibold hover:bg-white/10 transition-all">
              View Components
            </button>
          </div>
        </div>

        {/* Feature Grid */}
        <div className="max-w-7xl mx-auto mt-32 grid md:grid-cols-3 gap-8">
          {[
            { title: 'Vite & React', desc: 'Lightning fast development with the modern standard.' },
            { title: 'Supabase Ready', desc: 'Postgres database, Auth, and Realtime with zero config.' },
            { title: 'Tailwind CSS', desc: 'Pre-configured premium aesthetics for high authority UIs.' }
          ].map((feature, i) => (
            <div key={i} className="p-8 rounded-2xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
              <h3 className="text-xl font-bold mb-4">{feature.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </main>

      <footer className="py-20 border-t border-white/5 text-center text-slate-500 text-sm">
        &copy; 2026 SaaS Factory — Antigravity Industrial Engine
      </footer>
    </div>
  );
}

export default App;
