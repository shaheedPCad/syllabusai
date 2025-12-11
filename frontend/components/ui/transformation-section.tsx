'use client';

import { useRef, useEffect } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ArrowRight, Sparkles } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

export default function TransformationSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const subheadingRef = useRef<HTMLParagraphElement>(null);
  const inputRef = useRef<HTMLDivElement>(null);
  const outputRef = useRef<HTMLDivElement>(null);
  const arrowRef = useRef<HTMLDivElement>(null);
  const cursorRef = useRef<HTMLSpanElement>(null);

  useGSAP(
    () => {
      if (!headingRef.current || !inputRef.current || !outputRef.current) return;

      // Initial states
      gsap.set([headingRef.current, subheadingRef.current], {
        autoAlpha: 0,
        y: 30,
      });

      gsap.set(inputRef.current, {
        autoAlpha: 0,
        x: -50,
      });

      gsap.set(outputRef.current, {
        autoAlpha: 0,
        x: 50,
      });

      gsap.set(arrowRef.current, {
        autoAlpha: 0,
        scale: 0.8,
      });

      // Animation timeline
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 70%',
          end: 'top 20%',
          toggleActions: 'play none none reverse',
        },
        defaults: { ease: 'power3.out' },
      });

      tl.to(headingRef.current, {
        autoAlpha: 1,
        y: 0,
        duration: 0.8,
      })
        .to(
          subheadingRef.current,
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.8,
          },
          '-=0.6'
        )
        .to(
          inputRef.current,
          {
            autoAlpha: 1,
            x: 0,
            duration: 1,
          },
          '-=0.4'
        )
        .to(
          arrowRef.current,
          {
            autoAlpha: 1,
            scale: 1,
            duration: 0.6,
          },
          '-=0.5'
        )
        .to(
          outputRef.current,
          {
            autoAlpha: 1,
            x: 0,
            duration: 1,
          },
          '-=0.7'
        );

      // Pulsing cursor animation
      if (cursorRef.current) {
        gsap.to(cursorRef.current, {
          opacity: 0,
          duration: 0.8,
          repeat: -1,
          yoyo: true,
          ease: 'power2.inOut',
        });
      }

      // Floating arrow animation
      gsap.to(arrowRef.current, {
        x: 10,
        duration: 1.5,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      });
    },
    { scope: sectionRef }
  );

  // Shimmer effect for document lines
  useEffect(() => {
    const lines = document.querySelectorAll('.shimmer-line');
    lines.forEach((line, index) => {
      gsap.to(line, {
        backgroundPosition: '200% center',
        duration: 2,
        repeat: -1,
        ease: 'none',
        delay: index * 0.2,
      });
    });
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative z-10 w-full bg-transparent py-32 px-6 md:px-10 lg:px-16"
    >
      {/* Background spotlight effects */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/4 top-1/2 h-[600px] w-[600px] -translate-y-1/2 rounded-full bg-indigo-500/10 blur-[150px]" />
        <div className="absolute right-1/4 top-1/2 h-[600px] w-[600px] -translate-y-1/2 rounded-full bg-purple-500/10 blur-[150px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl">
        {/* Heading */}
        <div className="mb-20 text-center">
          <h2
            ref={headingRef}
            className="mb-6 text-5xl font-extralight leading-tight tracking-tight text-white sm:text-6xl md:text-7xl"
          >
            From a single thought to a full semester.
          </h2>
          <p
            ref={subheadingRef}
            className="mx-auto max-w-2xl text-lg font-light text-gray-400 sm:text-xl"
          >
            Type a topic. Get a comprehensive 12-week course structure in seconds.
          </p>
        </div>

        {/* Two Column Grid */}
        <div className="relative grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16">
          {/* Left Column: Input */}
          <div ref={inputRef} className="flex items-center justify-center">
            <div className="w-full max-w-xl">
              <div className="mb-4 flex items-center gap-2 text-sm font-light uppercase tracking-wider text-gray-500">
                <Sparkles size={16} className="text-indigo-400" />
                Input
              </div>

              {/* Glass Input Field */}
              <div className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-lg transition-all duration-500 hover:border-indigo-500/30 hover:bg-white/[0.07]">
                {/* Inner glow */}
                <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                  <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-transparent to-transparent" />
                </div>

                {/* Input content */}
                <div className="relative z-10">
                  <div className="mb-4 flex items-center gap-2 text-xs font-light uppercase tracking-wider text-gray-600">
                    Prompt
                  </div>
                  <p className="font-light leading-relaxed text-gray-300">
                    Create a syllabus for{' '}
                    <span className="text-indigo-300">'Introduction to AI Ethics'</span> for
                    college sophomores, focusing on{' '}
                    <span className="text-indigo-300">bias</span> and{' '}
                    <span className="text-indigo-300">privacy</span>.
                    <span
                      ref={cursorRef}
                      className="ml-1 inline-block h-5 w-0.5 bg-indigo-400"
                    />
                  </p>

                  {/* Generate button */}
                  <button className="mt-6 inline-flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-6 py-2.5 text-sm font-light text-indigo-300 transition-all duration-300 hover:border-indigo-500/50 hover:bg-indigo-500/20">
                    <Sparkles size={14} />
                    Generate
                  </button>
                </div>

                {/* Grain texture */}
                <div
                  className="pointer-events-none absolute inset-0 opacity-[0.015]"
                  style={{
                    backgroundImage:
                      'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' /%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\' /%3E%3C/svg%3E")',
                  }}
                />
              </div>
            </div>
          </div>

          {/* Animated Arrow Connection */}
          <div
            ref={arrowRef}
            className="absolute left-1/2 top-1/2 z-20 hidden -translate-x-1/2 -translate-y-1/2 lg:block"
          >
            <div className="relative">
              {/* Gradient line */}
              <div className="absolute left-0 top-1/2 h-0.5 w-24 -translate-y-1/2 bg-gradient-to-r from-indigo-500/50 via-purple-500/50 to-pink-500/50" />

              {/* Arrow icon with glow */}
              <div className="relative rounded-full border border-indigo-500/30 bg-indigo-500/10 p-3 backdrop-blur-lg">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 blur-md" />
                <ArrowRight className="relative z-10 text-indigo-300" size={20} />
              </div>

              {/* Flowing particles effect */}
              <div className="absolute left-0 top-1/2 h-1 w-1 -translate-y-1/2 animate-ping rounded-full bg-indigo-400" />
            </div>
          </div>

          {/* Right Column: Output */}
          <div ref={outputRef} className="flex items-center justify-center">
            <div className="w-full max-w-xl">
              <div className="mb-4 flex items-center gap-2 text-sm font-light uppercase tracking-wider text-gray-500">
                <Sparkles size={16} className="text-purple-400" />
                Output
              </div>

              {/* Floating Document */}
              <div className="group relative">
                {/* Spotlight effect behind document */}
                <div className="absolute inset-0 -z-10 scale-95 rounded-3xl bg-gradient-to-br from-purple-500/20 via-indigo-500/20 to-pink-500/20 blur-3xl transition-all duration-500 group-hover:scale-100" />

                {/* Document */}
                <div
                  className="relative overflow-hidden rounded-3xl border border-white/20 bg-white/10 p-8 shadow-2xl backdrop-blur-xl transition-all duration-500 hover:border-white/30"
                  style={{
                    transform: 'perspective(1000px) rotateY(-2deg) rotateX(2deg)',
                    transformStyle: 'preserve-3d',
                  }}
                >
                  {/* Document header */}
                  <div className="mb-6 border-b border-white/10 pb-4">
                    <h3 className="mb-2 text-2xl font-light tracking-tight text-white">
                      Course: AI Ethics 101
                    </h3>
                    <p className="text-sm font-light text-gray-400">
                      12-Week Comprehensive Structure
                    </p>
                  </div>

                  {/* Week items with shimmer effect */}
                  <div className="space-y-4">
                    {[
                      { week: 1, title: 'Algorithmic Bias', color: 'from-purple-400 to-pink-400' },
                      { week: 2, title: 'Data Privacy', color: 'from-indigo-400 to-purple-400' },
                      { week: 3, title: 'Surveillance Capitalism', color: 'from-blue-400 to-indigo-400' },
                      { week: 4, title: 'Fairness & Accountability', color: 'from-cyan-400 to-blue-400' },
                      { week: 5, title: 'Transparency & Explainability', color: 'from-teal-400 to-cyan-400' },
                    ].map((item, index) => (
                      <div
                        key={index}
                        className="shimmer-line relative overflow-hidden rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm"
                        style={{
                          backgroundImage: `linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)`,
                          backgroundSize: '200% 100%',
                          backgroundPosition: '-200% center',
                        }}
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br ${item.color} text-xs font-medium text-white shadow-lg`}
                          >
                            {item.week}
                          </div>
                          <span className="font-light text-gray-200">{item.title}</span>
                        </div>
                      </div>
                    ))}

                    {/* More indicator */}
                    <div className="pt-2 text-center">
                      <span className="text-xs font-light text-gray-500">
                        + 7 more weeks, assessments & resources
                      </span>
                    </div>
                  </div>

                  {/* Scanning line effect */}
                  <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/50 to-transparent opacity-50" />

                  {/* Corner accents */}
                  <div className="pointer-events-none absolute right-4 top-4 h-4 w-4 border-r border-t border-white/30" />
                  <div className="pointer-events-none absolute bottom-4 left-4 h-4 w-4 border-b border-l border-white/30" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </section>
  );
}

