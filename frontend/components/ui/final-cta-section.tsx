'use client';

import { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger, useGSAP);

export default function FinalCTASection() {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const subheadingRef = useRef<HTMLParagraphElement>(null);
  const buttonsRef = useRef<HTMLDivElement>(null);
  const microCopyRef = useRef<HTMLParagraphElement>(null);

  useGSAP(
    () => {
      if (!headingRef.current) return;

      // Initial states
      gsap.set([headingRef.current, subheadingRef.current, buttonsRef.current, microCopyRef.current], {
        autoAlpha: 0,
        y: 30,
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
          buttonsRef.current,
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.8,
          },
          '-=0.6'
        )
        .to(
          microCopyRef.current,
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.6,
          },
          '-=0.4'
        );
    },
    { scope: sectionRef }
  );

  return (
    <section
      ref={sectionRef}
      className="relative z-10 w-full bg-transparent py-32 px-6 md:px-10 lg:px-16"
    >
      {/* Horizon Line Glow Effect */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0">
        <div className="absolute bottom-0 left-1/2 h-64 w-[1400px] -translate-x-1/2 rounded-full bg-gradient-radial from-indigo-500/20 via-purple-500/10 to-transparent blur-3xl" />
        <div className="absolute bottom-0 left-1/2 h-32 w-full -translate-x-1/2 bg-gradient-to-t from-indigo-500/5 to-transparent" />
      </div>

      <div className="relative z-10 mx-auto max-w-4xl text-center">
        {/* Headline */}
        <h2
          ref={headingRef}
          className="mb-6 text-5xl font-extralight leading-tight tracking-tight text-white sm:text-6xl md:text-7xl"
        >
          Stop formatting. Start teaching.
        </h2>

        {/* Subheading */}
        <p
          ref={subheadingRef}
          className="mb-12 text-xl font-light leading-relaxed text-gray-300 sm:text-2xl"
        >
          Generate your first standards-aligned syllabus in under 60 seconds.
        </p>

        {/* Buttons */}
        <div
          ref={buttonsRef}
          className="mb-6 flex flex-wrap items-center justify-center gap-4"
        >
          {/* Primary Button - Glass + Glow */}
          <button className="rounded-full border border-white/20 bg-white/10 px-8 py-4 text-lg font-semibold tracking-tight text-white shadow-[0_0_20px_-5px_rgba(255,255,255,0.3)] backdrop-blur-md transition-all duration-300 hover:scale-105 hover:bg-white/20">
            Start Building Free
          </button>

          {/* Secondary Button - Ghost / Minimal */}
          <button className="rounded-full border border-transparent bg-transparent px-8 py-4 text-lg font-medium tracking-tight text-gray-400 transition-all duration-300 hover:bg-white/5 hover:text-white">
            Book a Demo
          </button>
        </div>

        {/* Micro-copy */}
        <p
          ref={microCopyRef}
          className="text-sm font-light text-gray-500"
        >
          No credit card required • Cancel anytime
        </p>
      </div>
    </section>
  );
}

