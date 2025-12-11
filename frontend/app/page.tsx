import Hero from "@/components/ui/neural-network-hero";
import FeaturesSection from "@/components/ui/features-section";
import TransformationSection from "@/components/ui/transformation-section";
import NeuralLinkSection from "@/components/ui/neural-link-section";
import PricingSection from "@/components/ui/pricing-section";
import FAQSection from "@/components/ui/faq-section";
import FinalCTASection from "@/components/ui/final-cta-section";
import Footer from "@/components/ui/footer";
import AnimatedBackground from "@/components/ui/animated-background";

export default function Home() {
  return (
    <>
      {/* Global Animated Background - Fixed behind all content */}
      <AnimatedBackground />
      
      {/* Global Dimmer Overlay - Uniform darkening across entire page */}
      <div className="fixed inset-0 z-[-1] bg-black/60 pointer-events-none" />
      
      {/* Page Content - Floats over the animated background */}
      <div className="relative w-full min-h-screen max-w-[100vw] overflow-x-hidden flex flex-col gap-0">
        <Hero 
          title="Curriculum design, reimagined."
          description="Transform vague ideas into comprehensive, standards-aligned syllabi in seconds. Built for educators who value pedagogy over paperwork."
          badgeText="AI Course Architect"
          badgeLabel="New"
          ctaButtons={[
            { text: "Start Building Free", href: "#get-started", primary: true },
            { text: "View Sample Syllabi", href: "#showcase" }
          ]}
          microDetails={["Standards Aligned", "Export to Canvas/Blackboard", "Bloom's Taxonomy Ready"]}
        />
        <FeaturesSection />
        <TransformationSection />
        <NeuralLinkSection />
        <PricingSection />
        <FAQSection />
        <FinalCTASection />
        <Footer />
      </div>
    </>
  );
}
