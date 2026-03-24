/**
 * Home.tsx — LogoClothz Scratch-Off Landing Page
 * ================================================
 * Design: Retro Carnival / Lottery Ticket
 * Palette: Deep Crimson bg (#8B1A1A), Aged Gold (#C9A84C), Cream (#FFF8E7)
 * Fonts: Playfair Display (headings) + Source Sans 3 (body)
 *
 * Layout: Full-viewport centered, single focal point — the scratch card.
 * Mobile-first, touch-enabled scratch interaction.
 */

import Confetti from "@/components/Confetti";
import ScratchCard from "@/components/ScratchCard";
import { useState } from "react";

const BG_IMAGE =
  "https://private-us-east-1.manuscdn.com/sessionFile/o5eg0MJ9CGxUQjpavK02gG/sandbox/5Qh2YJokDcDpUAA1uOMiI1-img-1_1771929873000_na1fn_bG9nb2Nsb3Roei1iZw.jpg?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbzVlZzBNSjlDR3hVUWpwYXZLMDJnRy9zYW5kYm94LzVRaDJZSm9rRGNEcFVBQTF1T01pSTEtaW1nLTFfMTc3MTkyOTg3MzAwMF9uYTFmbl9iRzluYjJOc2IzUm9laTFpWncuanBnP3gtb3NzLXByb2Nlc3M9aW1hZ2UvcmVzaXplLHdfMTkyMCxoXzE5MjAvZm9ybWF0LHdlYnAvcXVhbGl0eSxxXzgwIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=jPrqmz8--eHrN~pTe9zKgg2z3z~NM9X3Cc9VUAzWmfJjHIrHmWxy3pDmYk8zo56~r23JAMlwrmIFABnzZU1ZJXttauEBc5adJ3VFva5JTOt2QGGw5~APDvoo6LuQJ95EUSD0tceqH7YqSYK584NqGf-8sxW6vrEK5mu0SoKvqp~S4sE3qlzApN1qxaU7XmXEpa0KxjMJftKRQEcwrEbrlKBBOu4a~z0iMmMHibFGViUFIljIYmD6jYz0q5REMQ70eNhZ6nyJX6r~eqOUpxZ8wr2fEPKtu49i6wjTwAqnulcr68~ZfodVcoe8inYMVPR1Ia9LUE3OtOj4eCs8PiLSZg__";

export default function Home() {
  const [revealed, setRevealed] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);

  const handleRevealed = () => {
    setRevealed(true);
    setShowConfetti(true);
    // Stop confetti after 4 seconds
    setTimeout(() => setShowConfetti(false), 4500);
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden"
      style={{
        backgroundImage: `url(${BG_IMAGE})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      {/* Dark overlay for readability */}
      <div
        className="absolute inset-0"
        style={{ background: "rgba(20, 4, 4, 0.55)" }}
      />

      {/* Confetti */}
      {showConfetti && <Confetti />}

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center px-4 py-10 w-full max-w-lg mx-auto">

        {/* Logo / Brand */}
        <div className="mb-6 text-center">
          <p
            className="text-xs font-semibold tracking-[0.35em] uppercase mb-2"
            style={{ color: "#C9A84C", fontFamily: "'Source Sans 3', sans-serif" }}
          >
            Exclusive Offer from
          </p>
          <h1
            className="text-4xl sm:text-5xl font-black tracking-tight leading-none"
            style={{
              fontFamily: "'Playfair Display', serif",
              color: "#FFF8E7",
              textShadow: "0 2px 20px rgba(0,0,0,0.6)",
            }}
          >
            LogoClothz
          </h1>
          <div
            className="mt-2 mx-auto"
            style={{
              height: "2px",
              width: "60px",
              background: "linear-gradient(90deg, transparent, #C9A84C, transparent)",
            }}
          />
        </div>

        {/* Ticket card */}
        <div
          className="ticket-border rounded-2xl w-full"
          style={{
            background: "linear-gradient(160deg, rgba(30,6,6,0.92) 0%, rgba(50,12,12,0.95) 100%)",
            backdropFilter: "blur(8px)",
            padding: "28px 24px 32px",
          }}
        >
          {/* Ticket top row — hole punches */}
          <div className="flex items-center justify-between mb-5">
            <div className="hole-punch" />
            <div className="flex items-center gap-2">
              <span
                className="text-xs font-bold tracking-widest uppercase"
                style={{ color: "#C9A84C", fontFamily: "'Source Sans 3', sans-serif" }}
              >
                ✦ Official Discount Ticket ✦
              </span>
            </div>
            <div className="hole-punch" />
          </div>

          {/* Headline */}
          <div className="text-center mb-2">
            <p
              className="text-sm font-semibold tracking-widest uppercase"
              style={{ color: "#C9A84C", fontFamily: "'Source Sans 3', sans-serif" }}
            >
              You've been selected for
            </p>
            <h2
              className="text-5xl sm:text-6xl font-black leading-none mt-1"
              style={{
                fontFamily: "'Playfair Display', serif",
                background: "linear-gradient(135deg, #C9A84C 0%, #F5D98B 40%, #C9A84C 70%, #E8C547 100%)",
                backgroundSize: "200% auto",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                WebkitTextFillColor: "transparent",
                filter: "drop-shadow(0 2px 8px rgba(201,168,76,0.4))",
              }}
            >
              18% OFF
            </h2>
            <p
              className="text-sm mt-1"
              style={{ color: "#FFF8E7", fontFamily: "'Source Sans 3', sans-serif", opacity: 0.85 }}
            >
              Custom logo tablecloths — cut, sewn &amp; printed in the USA
            </p>
          </div>

          {/* Divider */}
          <div className="flex items-center gap-3 my-5">
            <div className="flex-1 h-px" style={{ background: "rgba(201,168,76,0.3)" }} />
            <span style={{ color: "#C9A84C", fontSize: "18px" }}>✦</span>
            <div className="flex-1 h-px" style={{ background: "rgba(201,168,76,0.3)" }} />
          </div>

          {/* Scratch card area */}
          <div className="flex flex-col items-center">
            {!revealed && (
              <p
                className="text-sm font-semibold mb-4 text-center"
                style={{ color: "#FFF8E7", fontFamily: "'Source Sans 3', sans-serif", opacity: 0.8 }}
              >
                👆 Scratch below to reveal your code
              </p>
            )}

            <div className="relative" style={{ marginBottom: revealed ? "0" : "36px" }}>
              <ScratchCard onRevealed={handleRevealed} />
            </div>

            {/* Post-reveal CTA */}
            {revealed && (
              <div className="animate-slide-up mt-8 w-full flex flex-col items-center gap-4">
                {/* Success message */}
                <div className="text-center">
                  <p
                    className="text-lg font-bold"
                    style={{ color: "#F5D98B", fontFamily: "'Playfair Display', serif" }}
                  >
                    🎉 You scratched it!
                  </p>
                  <p
                    className="text-sm mt-1"
                    style={{ color: "#FFF8E7", fontFamily: "'Source Sans 3', sans-serif", opacity: 0.8 }}
                  >
                    Use code <strong style={{ color: "#C9A84C" }}>LOGO18</strong> at checkout for 18% off
                  </p>
                </div>

                {/* Claim CTA button */}
                <a
                  href="https://logoclothz.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full text-center font-bold text-base py-4 px-8 rounded-xl transition-all duration-200 hover:scale-105 active:scale-95"
                  style={{
                    background: "linear-gradient(135deg, #C9A84C 0%, #F5D98B 50%, #C9A84C 100%)",
                    backgroundSize: "200% auto",
                    color: "#1A0505",
                    fontFamily: "'Source Sans 3', sans-serif",
                    letterSpacing: "0.05em",
                    boxShadow: "0 4px 24px rgba(201,168,76,0.5), 0 2px 8px rgba(0,0,0,0.4)",
                    textDecoration: "none",
                  }}
                >
                  Claim My 18% Discount →
                </a>

                {/* Fine print */}
                <p
                  className="text-xs text-center"
                  style={{ color: "#FFF8E7", fontFamily: "'Source Sans 3', sans-serif", opacity: 0.5 }}
                >
                  One-time use · Valid on logoclothz.com · While supplies last
                </p>
              </div>
            )}
          </div>

          {/* Ticket bottom row */}
          <div className="flex items-center justify-between mt-6">
            <div className="hole-punch" />
            <p
              className="text-xs tracking-widest"
              style={{ color: "rgba(201,168,76,0.4)", fontFamily: "'Source Sans 3', sans-serif" }}
            >
              logoclothz.com
            </p>
            <div className="hole-punch" />
          </div>
        </div>

        {/* Below ticket — trust signals */}
        <div className="mt-6 flex flex-wrap justify-center gap-4">
          {[
            { icon: "🇺🇸", text: "Cut, Sewn & Printed in the USA" },
            { icon: "🎨", text: "Full Custom Logo Print" },
            { icon: "🚚", text: "Fast Turnaround" },
          ].map((item) => (
            <div
              key={item.text}
              className="flex items-center gap-2 text-xs font-semibold"
              style={{ color: "#FFF8E7", fontFamily: "'Source Sans 3', sans-serif", opacity: 0.75 }}
            >
              <span>{item.icon}</span>
              <span>{item.text}</span>
            </div>
          ))}
        </div>

        {/* Footer */}
        <p
          className="mt-8 text-xs text-center"
          style={{ color: "rgba(255,248,231,0.35)", fontFamily: "'Source Sans 3', sans-serif" }}
        >
          © {new Date().getFullYear()} LogoClothz.com · All rights reserved
        </p>
      </div>
    </div>
  );
}
