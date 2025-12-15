"use client";

import { useEffect } from "react";
import Link from "next/link";
import { renderCanvas } from "@/components/ui/canvas"
import { Sparkles, ArrowRight, Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

export function Hero() {
  useEffect(() => {
    renderCanvas();
  }, []);

  return (
    <section id="home" className="relative min-h-screen overflow-hidden bg-white">
      <div className="animation-delay-8 animate-fadeIn mt-20 flex flex-col items-center justify-center px-4 text-center md:mt-20 relative z-10">
        <div className="z-10 mb-6 mt-10 sm:justify-center md:mb-4 md:mt-20">
          <div className="relative flex items-center whitespace-nowrap rounded-full border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 px-4 py-2 text-xs leading-6 text-blue-700 font-medium shadow-sm">
            ⚡ The AI Study Companion for Modern Students
          </div>
        </div>

        <div className="mb-10 mt-4  md:mt-6">
          <div className="px-2">
            <div className="border-ali relative mx-auto h-full max-w-7xl border p-6 [mask-image:radial-gradient(800rem_96rem_at_center,white,transparent)] md:px-12 md:py-20">
              <h1 className="flex select-none flex-col px-3 py-2 text-center text-5xl font-heading font-semibold leading-none tracking-tight md:flex-col md:text-8xl lg:flex-row lg:text-8xl">
                <Plus
                  strokeWidth={4}
                  className="text-ali absolute -left-5 -top-5 h-10 w-10"
                />
                <Plus
                  strokeWidth={4}
                  className="text-ali absolute -bottom-5 -left-5 h-10 w-10"
                />
                <Plus
                  strokeWidth={4}
                  className="text-ali absolute -right-5 -top-5 h-10 w-10"
                />
                <Plus
                  strokeWidth={4}
                  className="text-ali absolute -bottom-5 -right-5 h-10 w-10"
                />
                Turn Static PDFs into Active Learning.
              </h1>
              <div className="flex items-center justify-center gap-1">
                <span className="relative flex h-3 w-3 items-center justify-center">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-yellow-500 opacity-75"></span>
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-yellow-500"></span>
                </span>
                <p className="text-xs text-yellow-600">Under Development</p>
              </div>
            </div>
          </div>

          <p className="md:text-md mx-auto mb-16 mt-8 max-w-2xl px-6 text-sm text-primary/60 sm:px-6 md:max-w-4xl md:px-20 lg:text-lg">
            Stop drowning in files. Clarity instantly transforms your syllabus and lecture notes into interactive flashcards, quizzes, and a 24/7 AI tutor.
          </p>
          <div className="flex justify-center gap-2">
            <Link href={"/dashboard"}>
              <Button 
                variant="default" 
                size="lg"
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white"
              >
                Get Started for Free
              </Button>
            </Link>
            <Link href={"#demo"}>
              <Button 
                variant="outline" 
                size="lg"
                className="border-2 border-blue-600 text-blue-600 hover:bg-gradient-to-r hover:from-blue-600 hover:to-indigo-600 hover:text-white hover:border-transparent"
              >
                View Demo Course
              </Button>
            </Link>
          </div>
        </div>
      </div>
      <canvas
        className="pointer-events-none absolute top-0 left-0 w-full h-full z-0"
        id="canvas"
      ></canvas>
    </section>
  );
}

