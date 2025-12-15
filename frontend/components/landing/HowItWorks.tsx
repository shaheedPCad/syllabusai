"use client";

import { motion } from "framer-motion";
import { Upload, Brain, GraduationCap, FileText } from "lucide-react";

const steps = [
  {
    number: "01",
    badge: "Upload",
    title: "Drop in your materials.",
    description:
      "Upload your course syllabus, lecture slides, or messy notes. We support PDF, PPTX, and DOCX.",
    icon: Upload,
    visualType: "upload",
  },
  {
    number: "02",
    badge: "Analyze",
    title: "Let The Brain go to work.",
    description:
      "Our AI instantly reads, chunks, and connects concepts. It identifies dates, definitions, and key formulas in seconds.",
    icon: Brain,
    visualType: "processing",
  },
  {
    number: "03",
    badge: "Study",
    title: "Master the material.",
    description:
      "Start chatting with your course immediately. Generate flashcards for your commute or take a practice quiz to test your readiness.",
    icon: GraduationCap,
    visualType: "success",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3,
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

export default function HowItWorks() {
  return (
    <section className="w-full bg-slate-50 py-24 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="font-heading text-4xl sm:text-5xl md:text-6xl font-semibold text-slate-900 mb-4">
            How It Works
          </h2>
          <p className="text-lg sm:text-xl text-slate-500 max-w-2xl mx-auto">
            From upload to mastery in three simple steps.
          </p>
        </motion.div>

        {/* Steps */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="space-y-24"
        >
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isEven = index % 2 === 1;

            return (
              <motion.div
                key={index}
                variants={itemVariants}
                className="relative"
              >
                <div
                  className={`flex flex-col ${
                    isEven ? "lg:flex-row-reverse" : "lg:flex-row"
                  } items-center gap-12 lg:gap-16`}
                >
                  {/* Text Content */}
                  <div className="flex-1 relative z-10">
                    {/* Large Background Number */}
                    <div className="absolute -top-8 -left-4 lg:-left-8 text-8xl lg:text-9xl font-bold text-blue-600/10 select-none">
                      {step.number}
                    </div>

                    {/* Badge */}
                    <div className="inline-flex items-center px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-4">
                      {step.badge}
                    </div>

                    {/* Title */}
                    <h3 className="font-heading text-3xl sm:text-4xl font-semibold text-slate-900 mb-4 relative">
                      {step.title}
                    </h3>

                    {/* Description */}
                    <p className="text-lg text-slate-600 leading-relaxed max-w-xl">
                      {step.description}
                    </p>
                  </div>

                  {/* Visual Placeholder */}
                  <div className="flex-1 w-full max-w-md">
                    <motion.div
                      whileHover={{ scale: 1.02 }}
                      transition={{ duration: 0.2 }}
                      className="relative bg-white border-2 border-slate-200 rounded-2xl p-12 shadow-lg hover:shadow-xl transition-shadow duration-300"
                    >
                      {/* Visual Content */}
                      <div className="flex flex-col items-center justify-center space-y-6">
                        {/* Icon Circle */}
                        <div className="relative">
                          <div className="absolute inset-0 bg-blue-100 rounded-full blur-2xl opacity-60 animate-pulse"></div>
                          <div className="relative bg-gradient-to-br from-blue-50 to-blue-100 rounded-full p-8">
                            <Icon
                              className="w-16 h-16 text-blue-600"
                              strokeWidth={1.5}
                            />
                          </div>
                        </div>

                        {/* Visual Type Indicator */}
                        {step.visualType === "upload" && (
                          <div className="flex items-center gap-2 text-slate-400">
                            <FileText className="w-6 h-6" />
                            <div className="w-32 h-2 bg-slate-200 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: "0%" }}
                                whileInView={{ width: "100%" }}
                                viewport={{ once: true }}
                                transition={{ duration: 2, delay: 0.5 }}
                                className="h-full bg-blue-500 rounded-full"
                              />
                            </div>
                          </div>
                        )}

                        {step.visualType === "processing" && (
                          <div className="flex flex-col items-center gap-3">
                            <div className="flex gap-2">
                              {[0, 1, 2].map((i) => (
                                <motion.div
                                  key={i}
                                  animate={{
                                    scale: [1, 1.2, 1],
                                    opacity: [0.5, 1, 0.5],
                                  }}
                                  transition={{
                                    duration: 1.5,
                                    repeat: Infinity,
                                    delay: i * 0.2,
                                  }}
                                  className="w-3 h-3 bg-blue-500 rounded-full"
                                />
                              ))}
                            </div>
                            <span className="text-sm text-slate-500 font-medium">
                              Analyzing...
                            </span>
                          </div>
                        )}

                        {step.visualType === "success" && (
                          <div className="text-center">
                            <div className="text-5xl font-bold text-blue-600 mb-2">
                              A+
                            </div>
                            <div className="text-sm text-slate-500 font-medium">
                              Ready to ace your exam
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Decorative Corner Accent */}
                      <div className="absolute top-4 right-4 w-12 h-12 border-t-2 border-r-2 border-blue-200 rounded-tr-xl"></div>
                      <div className="absolute bottom-4 left-4 w-12 h-12 border-b-2 border-l-2 border-blue-200 rounded-bl-xl"></div>
                    </motion.div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
