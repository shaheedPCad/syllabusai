"use client";

import { motion } from "framer-motion";
import { MessageCircle, Zap, Brain } from "lucide-react";

const features = [
  {
    icon: MessageCircle,
    title: "Chat with your Course",
    description:
      "Don't Ctrl+F. Just ask. The AI understands every date, definition, and policy in your syllabus.",
  },
  {
    icon: Zap,
    title: "Instant Flashcards",
    description:
      "Turn lecture notes into study decks in one click. Perfect for memorizing terms and definitions.",
  },
  {
    icon: Brain,
    title: "Smart Quizzes",
    description:
      "Generate practice exams that look just like the real thing. Get instant feedback on why you missed a question.",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: "easeOut",
    },
  },
};

export default function Features() {
  return (
    <section className="w-full bg-white py-24 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="font-heading text-4xl sm:text-5xl md:text-6xl font-semibold text-slate-900 mb-4">
            Everything you need to ace the semester.
          </h2>
          <p className="text-lg sm:text-xl text-slate-500 max-w-2xl mx-auto">
            Clarity turns your passive course materials into active study tools.
          </p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                variants={itemVariants}
                whileHover={{
                  y: -5,
                  transition: { duration: 0.2 },
                }}
                className="group bg-white border border-slate-200 rounded-2xl p-8 transition-all duration-300 hover:shadow-xl hover:border-blue-100"
              >
                {/* Icon */}
                <div className="mb-6">
                  <div className="inline-flex items-center justify-center bg-blue-50 text-blue-600 rounded-xl p-3 transition-transform duration-300 group-hover:scale-110">
                    <Icon className="w-8 h-8" strokeWidth={1.5} />
                  </div>
                </div>

                {/* Content */}
                <h3 className="font-heading text-2xl font-semibold text-slate-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
