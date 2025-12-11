'use client';

import { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Check } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

interface PricingTier {
  id: string;
  name: string;
  price: string;
  priceDetail?: string;
  description: string;
  features: string[];
  buttonText: string;
  buttonStyle: 'ghost' | 'solid';
  badge?: string;
  highlighted?: boolean;
}

const pricingTiers: PricingTier[] = [
  {
    id: 'starter',
    name: 'Free',
    price: '$0',
    priceDetail: '/month',
    description: 'For individual teachers exploring AI.',
    features: [
      '1 Syllabus / Month',
      'Basic PDF Export',
      'Standard AI Model',
    ],
    buttonText: 'Start Building',
    buttonStyle: 'ghost',
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$12',
    priceDetail: '/month',
    description: 'For power users & department heads.',
    features: [
      'Unlimited Generations',
      'Direct LMS Sync (Canvas/Blackboard)',
      'Bloom\'s Taxonomy Analysis',
      'AI Policy Generator',
    ],
    buttonText: 'Get Pro Access',
    buttonStyle: 'solid',
    badge: 'Most Popular',
    highlighted: true,
  },
  {
    id: 'campus',
    name: 'Campus',
    price: 'Custom',
    description: 'For schools & districts requiring compliance.',
    features: [
      'SSO / SAML Integration',
      'FERPA/GDPR Compliance Contracts',
      'Admin Dashboard',
      'Custom AI Fine-tuning',
    ],
    buttonText: 'Contact Sales',
    buttonStyle: 'ghost',
  },
];

export default function PricingSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      if (!headingRef.current || !cardsRef.current) return;

      // Initial states
      gsap.set(headingRef.current, {
        autoAlpha: 0,
        y: 30,
      });

      const cards = cardsRef.current.querySelectorAll('.pricing-card');
      gsap.set(cards, {
        autoAlpha: 0,
        y: 50,
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
      }).to(
        cards,
        {
          autoAlpha: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
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
      {/* Floor light gradient */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0">
        <div className="absolute bottom-0 left-1/2 h-96 w-[1200px] -translate-x-1/2 rounded-full bg-gradient-radial from-indigo-500/10 via-purple-500/5 to-transparent blur-3xl" />
      </div>

      {/* Ambient glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/4 top-1/4 h-96 w-96 rounded-full bg-violet-500/5 blur-[120px]" />
        <div className="absolute right-1/4 bottom-1/4 h-96 w-96 rounded-full bg-indigo-500/5 blur-[120px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl">
        {/* Heading */}
        <div className="mb-20 text-center">
          <h2
            ref={headingRef}
            className="text-5xl font-extralight leading-tight tracking-tight text-white sm:text-6xl md:text-7xl"
          >
            Simple plans. Infinite curriculum.
          </h2>
        </div>

        {/* Pricing Grid */}
        <div
          ref={cardsRef}
          className="grid grid-cols-1 gap-8 md:grid-cols-3 md:items-center"
        >
          {pricingTiers.map((tier) => (
            <div
              key={tier.id}
              className={`pricing-card group relative ${
                tier.highlighted ? 'md:-mt-8 md:mb-8' : ''
              }`}
            >
              {/* Spotlight effect for Pro card */}
              {tier.highlighted && (
                <div className="pointer-events-none absolute inset-0 -z-10">
                  <div className="absolute inset-x-0 top-0 h-full w-full bg-gradient-to-b from-indigo-500/20 via-purple-500/10 to-transparent blur-3xl" />
                  <div className="absolute inset-0 bg-gradient-to-t from-transparent via-indigo-500/5 to-transparent" />
                </div>
              )}

              {/* Card */}
              <div
                className={`relative overflow-hidden rounded-3xl border backdrop-blur-xl transition-all duration-500 ${
                  tier.highlighted
                    ? 'border-white/20 bg-white/10 hover:border-white/30 hover:bg-white/[0.12] hover:shadow-2xl'
                    : 'border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/[0.08]'
                } ${tier.highlighted ? 'p-10' : 'p-8'}`}
              >
                {/* Badge for Pro */}
                {tier.badge && (
                  <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-4 py-1.5 backdrop-blur-sm">
                    <span className="text-xs font-light uppercase tracking-wider text-indigo-300">
                      {tier.badge}
                    </span>
                  </div>
                )}

                {/* Tier Name */}
                <h3 className="mb-3 text-2xl font-light tracking-tight text-white">
                  {tier.name}
                </h3>

                {/* Price */}
                <div className="mb-2 flex items-baseline gap-2">
                  <span className="text-5xl font-extralight tracking-tight text-white md:text-6xl">
                    {tier.price}
                  </span>
                  {tier.priceDetail && (
                    <span className="text-lg font-light text-gray-500">{tier.priceDetail}</span>
                  )}
                </div>

                {/* Description */}
                <p className="mb-8 text-sm font-light leading-relaxed text-gray-400">
                  {tier.description}
                </p>

                {/* Features List */}
                <ul className="mb-8 space-y-4">
                  {tier.features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-cyan-500/10">
                        <Check size={12} className="text-cyan-400" strokeWidth={3} />
                      </div>
                      <span className="text-sm font-light leading-relaxed text-gray-300">
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* CTA Button */}
                {tier.buttonStyle === 'solid' ? (
                  <button className="w-full rounded-2xl border border-white bg-white px-6 py-4 text-sm font-medium tracking-tight text-black transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-white/20">
                    {tier.buttonText}
                  </button>
                ) : (
                  <button className="w-full rounded-2xl border border-white/20 bg-transparent px-6 py-4 text-sm font-light tracking-tight text-white transition-all duration-300 hover:border-white/40 hover:bg-white/5">
                    {tier.buttonText}
                  </button>
                )}

                {/* Hover glow effect */}
                <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                  <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent" />
                  <div className="absolute -inset-px rounded-3xl bg-gradient-to-br from-white/10 via-transparent to-transparent opacity-50 blur-sm" />
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
          ))}
        </div>

        {/* Additional Info */}
        <div className="mt-16 text-center">
          <p className="text-sm font-light text-gray-500">
            All plans include SSL encryption, automatic backups, and responsive support.
          </p>
        </div>
      </div>

    </section>
  );
}

