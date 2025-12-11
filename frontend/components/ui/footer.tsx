'use client';

import { Github, Linkedin, Twitter } from 'lucide-react';

const footerLinks = {
  product: [
    { name: 'Features', href: '#features' },
    { name: 'Integrations', href: '#integrations' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'Changelog', href: '#changelog' },
  ],
  resources: [
    { name: 'Blog', href: '#blog' },
    { name: 'Community', href: '#community' },
    { name: 'Help Center', href: '#help' },
    { name: 'API Docs', href: '#api' },
  ],
  legal: [
    { name: 'Privacy', href: '#privacy' },
    { name: 'Terms', href: '#terms' },
    { name: 'Security', href: '#security' },
    { name: 'DPA', href: '#dpa' },
  ],
};

const socialLinks = [
  { name: 'Twitter', icon: Twitter, href: '#twitter' },
  { name: 'GitHub', icon: Github, href: '#github' },
  { name: 'LinkedIn', icon: Linkedin, href: '#linkedin' },
];

export default function Footer() {
  return (
    <footer className="relative z-10 w-full border-t border-white/5 bg-transparent px-6 py-16 md:px-10 lg:px-16">
      <div className="mx-auto max-w-7xl">
        {/* Main Footer Grid */}
        <div className="grid grid-cols-1 gap-12 md:grid-cols-2 lg:grid-cols-4">
          {/* Column 1: Brand */}
          <div className="space-y-4">
            <h3 className="text-xl font-light tracking-tight text-white">
              Syllabus AI
            </h3>
            <p className="font-mono text-xs leading-relaxed text-gray-600">
              Architecting the future of curriculum.
            </p>
          </div>

          {/* Column 2: Product */}
          <div className="space-y-4">
            <h4 className="font-mono text-xs font-medium uppercase tracking-wider text-gray-500">
              Product
            </h4>
            <ul className="space-y-3">
              {footerLinks.product.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="font-mono text-sm text-gray-600 transition-colors duration-300 hover:text-white"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: Resources */}
          <div className="space-y-4">
            <h4 className="font-mono text-xs font-medium uppercase tracking-wider text-gray-500">
              Resources
            </h4>
            <ul className="space-y-3">
              {footerLinks.resources.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="font-mono text-sm text-gray-600 transition-colors duration-300 hover:text-white"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4: Legal */}
          <div className="space-y-4">
            <h4 className="font-mono text-xs font-medium uppercase tracking-wider text-gray-500">
              Legal
            </h4>
            <ul className="space-y-3">
              {footerLinks.legal.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="font-mono text-sm text-gray-600 transition-colors duration-300 hover:text-white"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-16 flex flex-col items-center justify-between gap-6 border-t border-white/5 pt-8 md:flex-row">
          {/* Copyright */}
          <p className="font-mono text-xs text-gray-600">
            © 2024 Syllabus AI Inc.
          </p>

          {/* Social Links */}
          <div className="flex items-center gap-6">
            {socialLinks.map((social) => {
              const Icon = social.icon;
              return (
                <a
                  key={social.name}
                  href={social.href}
                  className="text-gray-600 transition-colors duration-300 hover:text-white"
                  aria-label={social.name}
                >
                  <Icon size={18} strokeWidth={1.5} />
                </a>
              );
            })}
          </div>
        </div>
      </div>
    </footer>
  );
}

