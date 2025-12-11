'use client';

import { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { RefreshCw, Award, Shield, BookOpen } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  className?: string;
}

function FeatureCard({ title, description, icon, className = '' }: FeatureCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={cardRef}
      className={`group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-lg transition-all duration-500 hover:border-white/20 hover:bg-white/[0.07] ${className}`}
    >
      {/* Glow effect on hover */}
      <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
        <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent" />
        <div className="absolute -inset-px rounded-3xl bg-gradient-to-br from-white/20 via-transparent to-transparent opacity-50 blur-sm" />
      </div>

      <div className="relative z-10">
        <div className="mb-6 inline-flex rounded-2xl border border-white/10 bg-white/5 p-3 backdrop-blur-sm">
          <div className="text-white/80 transition-colors duration-300 group-hover:text-white">
            {icon}
          </div>
        </div>

        <h3 className="mb-3 text-2xl font-light tracking-tight text-white">
          {title}
        </h3>

        <p className="text-base font-light leading-relaxed text-gray-400">
          {description}
        </p>
      </div>

      {/* Subtle grain texture */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.015]" style={{
        backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' /%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\' /%3E%3C/svg%3E")'
      }} />
    </div>
  );
}

export default function FeaturesSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      if (!headingRef.current || !gridRef.current) return;

      const cards = gridRef.current.querySelectorAll('.feature-card');

      gsap.set([headingRef.current, ...Array.from(cards)], {
        autoAlpha: 0,
        y: 30,
      });

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 80%',
          end: 'top 20%',
          toggleActions: 'play none none reverse',
        },
        defaults: { ease: 'power3.out' },
      });

      tl.to(headingRef.current, {
        autoAlpha: 1,
        y: 0,
        duration: 0.8,
      }).to(
        cards,
        {
          autoAlpha: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.1,
        },
        '-=0.5'
      );
    },
    { scope: sectionRef, dependencies: [] }
  );

  return (
    <section
      ref={sectionRef}
      className="relative z-10 w-full bg-transparent py-32 px-6 md:px-10 lg:px-16"
    >
      {/* Background glow effects */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/4 top-0 h-96 w-96 rounded-full bg-purple-500/10 blur-[120px]" />
        <div className="absolute right-1/4 bottom-0 h-96 w-96 rounded-full bg-blue-500/10 blur-[120px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl">
        {/* Section Heading */}
        <h2
          ref={headingRef}
          className="mb-16 text-center text-5xl font-extralight leading-tight tracking-tight text-white sm:text-6xl md:text-7xl"
        >
          Intelligence meets Pedagogy.
        </h2>

        {/* Bento Grid */}
        <div
          ref={gridRef}
          className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4 lg:grid-rows-2"
        >
          {/* Card 1: Wide (spans 2 cols) */}
          <FeatureCard
            className="feature-card lg:col-span-2"
            title="Native LMS Sync"
            description="Push your entire course structure, quizzes, and reading lists directly to Canvas, Blackboard, or Moodle with one click."
            icon={<RefreshCw size={24} className="transition-transform duration-500 group-hover:rotate-180" />}
          />

          {/* Card 2: Tall (spans 2 rows) */}
          <FeatureCard
            className="feature-card lg:row-span-2"
            title="Accreditation Ready"
            description="Every learning objective is automatically mapped to Bloom's Taxonomy and state standards. Audit-proof your curriculum."
            icon={<Award size={24} />}
          />

          {/* Card 3: Small */}
          <FeatureCard
            className="feature-card"
            title="Ethical Guardrails"
            description="Auto-generate AI use policies specific to your class."
            icon={<Shield size={24} />}
          />

          {/* Card 4: Small (bottom right) */}
          <FeatureCard
            className="feature-card lg:col-start-2"
            title="Dynamic Readings"
            description="AI agents source peer-reviewed texts to match your topics."
            icon={<BookOpen size={24} />}
          />
        </div>
      </div>

    </section>
  );
}

