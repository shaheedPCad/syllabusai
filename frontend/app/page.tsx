import { Hero } from "@/components/ui/hero";
import Features from "@/components/landing/Features";
import HowItWorks from "@/components/landing/HowItWorks";
import AboutSection from "@/components/landing/AboutSection";
import Pricing from "@/components/landing/Pricing";
import CTA from "@/components/landing/CTA";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <div className="relative w-full min-h-screen max-w-[100vw] overflow-x-hidden">
      <Hero />
      <Features />
      <HowItWorks />
      <AboutSection />
      <Pricing />
      <CTA />
      <Footer />
    </div>
  );
}
