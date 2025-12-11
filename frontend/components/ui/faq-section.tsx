'use client';

import { useRef, useState } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Plus } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

interface FAQItem {
  question: string;
  answer: string;
}

const faqItems: FAQItem[] = [
  {
    question: "Do you train on my course data?",
    answer: "No. Your intellectual property remains yours. We use a zero-retention API architecture, meaning your course inputs are processed and then discarded."
  },
  {
    question: "Is this considered AI plagiarism?",
    answer: "Syllabus AI is an administrative tool, not a content writer. It structures your semester, dates, and policies. You still provide the lecture content and pedagogical voice."
  },
  {
    question: "Does it work with my university's template?",
    answer: "Yes. You can upload your department's required boilerplate (PDF/Docx), and our system will weave it seamlessly into the generated schedule."
  },
  {
    question: "Can students access this?",
    answer: "This is an instructor-only tool. However, you can use our 'Policy Generator' to create clear AI guidelines for your students."
  }
];

interface AccordionItemProps {
  item: FAQItem;
  index: number;
  isOpen: boolean;
  onToggle: () => void;
}

function AccordionItem({ item, index, isOpen, onToggle }: AccordionItemProps) {
  const contentRef = useRef<HTMLDivElement>(null);
  const iconRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      if (!contentRef.current || !iconRef.current) return;

      if (isOpen) {
        gsap.to(contentRef.current, {
          height: 'auto',
          opacity: 1,
          duration: 0.4,
          ease: 'power3.out',
        });
        gsap.to(iconRef.current, {
          rotation: 45,
          duration: 0.3,
          ease: 'power2.out',
        });
      } else {
        gsap.to(contentRef.current, {
          height: 0,
          opacity: 0,
          duration: 0.3,
          ease: 'power2.in',
        });
        gsap.to(iconRef.current, {
          rotation: 0,
          duration: 0.3,
          ease: 'power2.out',
        });
      }
    },
    { dependencies: [isOpen] }
  );

  return (
    <div
      className={`group relative overflow-hidden rounded-2xl border backdrop-blur-lg transition-all duration-500 ${
        isOpen
          ? 'border-indigo-500/40 bg-white/10 shadow-lg shadow-indigo-500/10'
          : 'border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/[0.07]'
      }`}
    >
      {/* Question Button */}
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between gap-4 p-6 text-left transition-colors duration-300"
      >
        <span className="text-lg font-medium tracking-tight text-white">
          {item.question}
        </span>
        <div
          ref={iconRef}
          className={`flex-shrink-0 rounded-full p-1 transition-colors duration-300 ${
            isOpen ? 'bg-indigo-500/20 text-indigo-300' : 'bg-white/10 text-white/60'
          }`}
        >
          <Plus size={20} strokeWidth={2} />
        </div>
      </button>

      {/* Answer Content */}
      <div
        ref={contentRef}
        className="overflow-hidden"
        style={{ height: 0, opacity: 0 }}
      >
        <div className="border-t border-white/10 px-6 pb-6 pt-4">
          <p className="font-light leading-relaxed text-gray-400">
            {item.answer}
          </p>
        </div>
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
  );
}

export default function FAQSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const subheadingRef = useRef<HTMLParagraphElement>(null);
  const accordionRef = useRef<HTMLDivElement>(null);
  
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const handleToggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  useGSAP(
    () => {
      if (!headingRef.current || !accordionRef.current) return;

      // Initial states
      gsap.set([headingRef.current, subheadingRef.current], {
        autoAlpha: 0,
        y: 30,
      });

      const items = accordionRef.current.querySelectorAll('.faq-item');
      gsap.set(items, {
        autoAlpha: 0,
        y: 20,
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
          items,
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.1,
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
      <div className="relative z-10 mx-auto max-w-3xl">
        {/* Heading */}
        <div className="mb-16 text-center">
          <h2
            ref={headingRef}
            className="mb-6 text-4xl font-extralight leading-tight tracking-tight text-white sm:text-5xl md:text-6xl"
          >
            Built for the classroom, not the chatroom.
          </h2>
          <p
            ref={subheadingRef}
            className="text-lg font-light text-gray-400 sm:text-xl"
          >
            Privacy-first architecture designed for academic compliance.
          </p>
        </div>

        {/* FAQ Accordion */}
        <div ref={accordionRef} className="space-y-4">
          {faqItems.map((item, index) => (
            <div key={index} className="faq-item">
              <AccordionItem
                item={item}
                index={index}
                isOpen={openIndex === index}
                onToggle={() => handleToggle(index)}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

