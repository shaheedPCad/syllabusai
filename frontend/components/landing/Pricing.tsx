"use client";

import { motion } from "framer-motion";
import { CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const plans = [
  {
    name: "The Crammer",
    price: "$0",
    period: "month",
    description: "Perfect for trying out the platform.",
    features: [
      "1 Course per semester",
      "50 AI Flashcards / month",
      "Basic Chat Support",
      "Upload PDF & Docx",
    ],
    buttonText: "Start Learning Free",
    buttonVariant: "outline" as const,
    highlighted: false,
  },
  {
    name: "The Scholar",
    price: "$9",
    period: "month",
    description: "For students who want to master every subject.",
    features: [
      "Unlimited Courses",
      "Unlimited Flashcards & Quizzes",
      "GPT-4o Advanced Reasoning",
      "Priority Processing",
    ],
    buttonText: "Get Pro Access",
    buttonVariant: "default" as const,
    highlighted: true,
    badge: "Most Popular",
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

const cardVariants = {
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

export default function Pricing() {
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
            Fair pricing for every student.
          </h2>
          <p className="text-lg sm:text-xl text-slate-500 max-w-2xl mx-auto">
            Start for free. Upgrade when you need more power.
          </p>
        </motion.div>

        {/* Pricing Cards */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto"
        >
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              variants={cardVariants}
              className="relative"
            >
              {/* Most Popular Badge */}
              {plan.highlighted && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                  <div className="inline-flex items-center px-4 py-1.5 bg-blue-600 text-white rounded-full text-sm font-medium shadow-lg">
                    {plan.badge}
                  </div>
                </div>
              )}

              {/* Card */}
              <div
                className={`relative h-full rounded-2xl border-2 p-8 transition-all duration-300 hover:shadow-xl ${
                  plan.highlighted
                    ? "border-blue-200 bg-blue-50/30 shadow-lg"
                    : "border-slate-200 bg-white hover:border-blue-100"
                }`}
              >
                {/* Plan Name */}
                <h3 className="font-heading text-2xl font-semibold text-slate-900 mb-2">
                  {plan.name}
                </h3>

                {/* Price */}
                <div className="mb-4">
                  <span className="text-5xl font-bold text-slate-900">
                    {plan.price}
                  </span>
                  <span className="text-slate-500 text-lg ml-2">
                    / {plan.period}
                  </span>
                </div>

                {/* Description */}
                <p className="text-slate-600 mb-6">{plan.description}</p>

                {/* Features List */}
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li
                      key={featureIndex}
                      className="flex items-start gap-3"
                    >
                      <CheckCircle2
                        className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5"
                        strokeWidth={2}
                      />
                      <span className="text-slate-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* CTA Button */}
                <Link href="/dashboard" className="block">
                  <Button
                    variant={plan.buttonVariant}
                    size="lg"
                    className={`w-full ${
                      plan.highlighted
                        ? "bg-blue-600 hover:bg-blue-700 text-white"
                        : ""
                    }`}
                  >
                    {plan.buttonText}
                  </Button>
                </Link>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom Note */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center mt-12"
        >
          <p className="text-sm text-slate-500">
            All plans include 7-day money-back guarantee. Cancel anytime.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
