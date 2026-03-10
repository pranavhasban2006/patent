import { Code2, Network } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Hero() {
    return (
        <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full pt-16 pb-12 px-6 flex flex-col items-center justify-center text-center relative overflow-hidden"
        >
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-2xl h-64 bg-indigo-500/20 blur-[120px] -z-10 rounded-full" />

            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-indigo-500/20 rounded-2xl border border-indigo-500/30">
                    <Network className="w-8 h-8 text-indigo-400" />
                </div>
                <div className="p-3 bg-violet-500/20 rounded-2xl border border-violet-500/30">
                    <Code2 className="w-8 h-8 text-violet-400" />
                </div>
            </div>

            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-violet-400 to-fuchsia-400">
                Semantic Impact Engine
            </h1>

            <p className="max-w-xl text-lg text-slate-400 font-medium">
                A deterministic, Datalog-powered analysis tool. Enter your code, specify a changed element, and securely trace logical impact throughout your entire graph.
            </p>
        </motion.div>
    );
}
