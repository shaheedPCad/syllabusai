'use client';

import { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger, useGSAP);

interface OrbitingNode {
  id: string;
  name: string;
  logo: React.ReactNode;
  angle: number;
  color: string;
}

// Platform Logo Components
const CanvasLogo = () => (
  <svg viewBox="0 0 48 48" className="h-8 w-8" fill="currentColor">
    <path d="M24 4L4 14v20l20 10 20-10V14L24 4zm0 4.84L39.32 16 24 23.16 8.68 16 24 8.84zM8 19.32l14 7v14.36l-14-7V19.32zm30 14.36l-14 7V26.32l14-7v14.36z"/>
  </svg>
);

const BlackboardLogo = () => (
  <svg viewBox="0 0 48 48" className="h-8 w-8" fill="currentColor">
    <rect x="6" y="8" width="36" height="28" rx="2"/>
    <path d="M6 12h36M12 16h6M12 20h10M12 24h8M12 28h12M24 16h12M24 20h10M24 24h12M24 28h8"/>
    <rect x="20" y="36" width="8" height="2"/>
    <path d="M16 38h16v2H16z"/>
  </svg>
);

const GoogleDriveLogo = () => (
  <svg viewBox="0 0 48 48" className="h-8 w-8" fill="currentColor">
    <path d="M15.5 4L4 24l7.75 13.5h24.5L44 24 32.5 4h-17z"/>
    <path d="M24 17l-8.5 14.7h17L24 17z" opacity="0.5"/>
  </svg>
);

const MoodleLogo = () => (
  <svg viewBox="0 0 48 48" className="h-8 w-8" fill="currentColor">
    <circle cx="24" cy="24" r="18"/>
    <path d="M24 10v28M10 24h28M17 17l14 14M17 31l14-14" stroke="black" strokeWidth="2" opacity="0.3"/>
  </svg>
);

const NotionLogo = () => (
  <svg viewBox="0 0 48 48" className="h-8 w-8" fill="currentColor">
    <path d="M8 4h28l4 4v32l-4 4H12l-4-4V8l4-4z"/>
    <path d="M16 14h16v2H16zm0 6h20v2H16zm0 6h18v2H16zm0 6h14v2H16z" fill="black" opacity="0.4"/>
  </svg>
);

const ZoomLogo = () => (
  <svg viewBox="0 0 48 48" className="h-8 w-8" fill="currentColor">
    <rect x="6" y="12" width="24" height="18" rx="3"/>
    <path d="M30 16l12-6v22l-12-6V16z"/>
  </svg>
);

const integrations: OrbitingNode[] = [
  { id: 'canvas', name: 'Canvas', logo: <CanvasLogo />, angle: -90, color: '#E13F2B' },
  { id: 'blackboard', name: 'Blackboard', logo: <BlackboardLogo />, angle: -30, color: '#000000' },
  { id: 'google-drive', name: 'Google Drive', logo: <GoogleDriveLogo />, angle: 30, color: '#4285F4' },
  { id: 'moodle', name: 'Moodle', logo: <MoodleLogo />, angle: 90, color: '#F98012' },
  { id: 'notion', name: 'Notion', logo: <NotionLogo />, angle: 150, color: '#000000' },
  { id: 'zoom', name: 'Zoom', logo: <ZoomLogo />, angle: 210, color: '#2D8CFF' },
];

export default function NeuralLinkSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const constellationRef = useRef<HTMLDivElement>(null);
  const centralNodeRef = useRef<HTMLDivElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const subheadingRef = useRef<HTMLParagraphElement>(null);

  useGSAP(
    () => {
      if (!constellationRef.current || !centralNodeRef.current) return;

      // Initial states
      gsap.set(constellationRef.current, {
        autoAlpha: 0,
        scale: 0.8,
      });

      gsap.set([headingRef.current, subheadingRef.current], {
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

      tl.to(constellationRef.current, {
        autoAlpha: 1,
        scale: 1,
        duration: 1.2,
      })
        .to(
          headingRef.current,
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.8,
          },
          '-=0.6'
        )
        .to(
          subheadingRef.current,
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.8,
          },
          '-=0.6'
        );

      // Breathing animation for central node (heartbeat effect)
      gsap.to(centralNodeRef.current, {
        scale: 1.08,
        duration: 2,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      });

      // Breathing animation for the outer ring
      const outerRing = centralNodeRef.current?.querySelector('.outer-ring');
      if (outerRing) {
        gsap.to(outerRing, {
          scale: 1.1,
          opacity: 0.3,
          duration: 2,
          repeat: -1,
          yoyo: true,
          ease: 'sine.inOut',
        });
      }

      // Animate data pulses along the lines
      integrations.forEach((_, index) => {
        const pulse = document.querySelector(`.pulse-${index}`);
        if (pulse) {
          gsap.to(pulse, {
            attr: { offset: '100%' },
            duration: 2.5,
            repeat: -1,
            ease: 'none',
            delay: index * 0.4,
          });
        }
      });
    },
    { scope: sectionRef, dependencies: [] }
  );

  // Calculate positions for orbiting nodes
  const radius = 280; // Increased distance from center
  const mobileRadius = 160; // Smaller radius for mobile

  return (
    <section
      ref={sectionRef}
      className="relative z-10 w-full bg-transparent py-32 px-6 md:px-10 lg:px-16"
    >
      {/* Enhanced Nebula Effect */}
      <div className="pointer-events-none absolute inset-0">
        {/* Large central nebula */}
        <div className="absolute left-1/2 top-[300px] h-[1000px] w-[1000px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#4c1d95] opacity-10 blur-[150px]" />
        <div className="absolute left-1/2 top-[300px] h-[800px] w-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-radial from-purple-500/15 via-indigo-500/10 to-transparent blur-3xl" />
        <div className="absolute left-1/2 top-[300px] h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-radial from-violet-500/20 via-indigo-500/10 to-transparent blur-2xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl">
        {/* Constellation Container */}
        <div
          ref={constellationRef}
          className="relative mx-auto mb-20 flex h-[500px] items-center justify-center md:h-[700px]"
        >
          <svg
            className="absolute inset-0 h-full w-full"
            style={{ overflow: 'visible' }}
            viewBox="0 0 1000 1000"
            preserveAspectRatio="xMidYMid meet"
          >
            <defs>
              <filter id="glow">
                <feGaussianBlur stdDeviation="4" result="coloredBlur" />
                <feMerge>
                  <feMergeNode in="coloredBlur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
              
              {/* Gradient for connection lines */}
              <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="transparent" stopOpacity="0" />
                <stop offset="40%" stopColor="rgba(255, 255, 255, 0.2)" stopOpacity="1" />
                <stop offset="60%" stopColor="rgba(255, 255, 255, 0.2)" stopOpacity="1" />
                <stop offset="100%" stopColor="transparent" stopOpacity="0" />
              </linearGradient>

              {/* Animated pulse gradient */}
              <radialGradient id="pulseGradient">
                <stop offset="0%" stopColor="#8b5cf6" stopOpacity="1" />
                <stop offset="50%" stopColor="#06b6d4" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#ec4899" stopOpacity="0" />
              </radialGradient>
            </defs>

            {/* Connection lines with animated pulses */}
            {integrations.map((integration, index) => {
              const angle = (integration.angle * Math.PI) / 180;
              const x1 = 500;
              const y1 = 500;
              const x2 = 500 + radius * Math.cos(angle);
              const y2 = 500 + radius * Math.sin(angle);

              return (
                <g key={`connection-${integration.id}`} className={`connection-group-${index}`}>
                  {/* Base line with gradient */}
                  <line
                    x1={x1}
                    y1={y1}
                    x2={x2}
                    y2={y2}
                    stroke="url(#lineGradient)"
                    strokeWidth="1"
                    className="connection-line transition-all duration-500"
                    data-index={index}
                  />

                  {/* Animated pulse traveling along the line */}
                  <line
                    x1={x1}
                    y1={y1}
                    x2={x2}
                    y2={y2}
                    stroke="url(#pulseGradient)"
                    strokeWidth="3"
                    strokeDasharray="20 1000"
                    strokeLinecap="round"
                    filter="url(#glow)"
                    className={`pulse-${index}`}
                  >
                    <animate
                      attributeName="stroke-dashoffset"
                      from="0"
                      to="-1020"
                      dur="2.5s"
                      repeatCount="indefinite"
                      begin={`${index * 0.4}s`}
                    />
                    <animate
                      attributeName="opacity"
                      values="0;1;1;0"
                      dur="2.5s"
                      repeatCount="indefinite"
                      begin={`${index * 0.4}s`}
                    />
                  </line>
                </g>
              );
            })}
          </svg>

          {/* Central Node - Syllabus AI (Enhanced) */}
          <div
            ref={centralNodeRef}
            className="relative z-20 flex h-48 w-48 items-center justify-center rounded-full border-2 border-white/30 bg-white/10 shadow-2xl backdrop-blur-md md:h-56 md:w-56"
          >
            {/* Breathing outer ring */}
            <div className="outer-ring absolute -inset-4 rounded-full border-2 border-white/20 opacity-50" />
            
            {/* Inner gradient background */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20" />
            
            {/* Inner glow rings */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-white/20 to-transparent opacity-50" />
            <div className="absolute inset-6 rounded-full border border-white/20" />
            <div className="absolute inset-12 rounded-full border border-white/10" />

            {/* Pulsing glow effect */}
            <div className="absolute inset-0 -z-10 rounded-full bg-gradient-to-br from-indigo-500/40 to-purple-500/40 blur-2xl" />

            {/* Content */}
            <div className="relative z-10 text-center">
              <div className="mb-3 text-4xl">🧠</div>
              <p className="text-base font-light text-white md:text-lg">Syllabus AI</p>
            </div>
          </div>

          {/* Orbiting Nodes with Real Logos */}
          <div className="hidden md:block">
            {integrations.map((integration, index) => {
              const angle = (integration.angle * Math.PI) / 180;
              const x = radius * Math.cos(angle);
              const y = radius * Math.sin(angle);

              return (
                <div
                  key={integration.id}
                  className="orbiting-node group absolute z-10 cursor-pointer"
                  style={{
                    left: '50%',
                    top: '50%',
                    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
                  }}
                  onMouseEnter={() => {
                    const line = document.querySelector(`.connection-line[data-index="${index}"]`);
                    if (line) {
                      line.setAttribute('stroke', 'rgba(255, 255, 255, 0.6)');
                      line.setAttribute('stroke-width', '2');
                    }
                  }}
                  onMouseLeave={() => {
                    const line = document.querySelector(`.connection-line[data-index="${index}"]`);
                    if (line) {
                      line.setAttribute('stroke', 'url(#lineGradient)');
                      line.setAttribute('stroke-width', '1');
                    }
                  }}
                >
                  <div className="relative flex h-28 w-28 items-center justify-center rounded-full border border-white/10 bg-white/5 backdrop-blur-lg transition-all duration-500 group-hover:scale-110 group-hover:border-white/30 group-hover:bg-white group-hover:shadow-2xl">
                    {/* Hover glow */}
                    <div 
                      className="absolute inset-0 -z-10 rounded-full opacity-0 blur-xl transition-opacity duration-500 group-hover:opacity-100"
                      style={{ backgroundColor: `${integration.color}40` }}
                    />

                    {/* Logo */}
                    <div 
                      className="text-white/60 transition-all duration-300 group-hover:text-white"
                      style={{ color: 'inherit' }}
                    >
                      <div className="group-hover:hidden">
                        {integration.logo}
                      </div>
                      <div className="hidden group-hover:block" style={{ color: integration.color }}>
                        {integration.logo}
                      </div>
                    </div>

                    {/* Label */}
                    <div className="absolute -bottom-10 left-1/2 -translate-x-1/2 whitespace-nowrap text-sm font-light text-gray-400 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                      {integration.name}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Mobile: Horizontal scrolling row */}
          <div className="absolute inset-x-0 top-full mt-12 block md:hidden">
            <div className="flex gap-6 overflow-x-auto px-6 pb-4">
              {integrations.map((integration) => (
                <div
                  key={integration.id}
                  className="flex-shrink-0"
                >
                  <div className="flex h-24 w-24 flex-col items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur-lg">
                    <div className="text-white/60" style={{ color: integration.color }}>
                      {integration.logo}
                    </div>
                    <p className="text-xs font-light text-gray-400">{integration.name}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Typography */}
        <div className="text-center">
          <h2
            ref={headingRef}
            className="mb-6 text-5xl font-extralight leading-tight tracking-tight text-white sm:text-6xl md:text-7xl"
          >
            Plug directly into your ecosystem.
          </h2>
          <p
            ref={subheadingRef}
            className="mx-auto max-w-3xl text-lg font-light leading-relaxed text-gray-400 sm:text-xl"
          >
            Don't just generate text. Push structured modules, assignments, and reading
            lists directly to your LMS in one click.
          </p>
        </div>
      </div>

    </section>
  );
}

