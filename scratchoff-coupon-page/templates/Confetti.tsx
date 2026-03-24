/**
 * Confetti.tsx
 * ============
 * Design: Retro Carnival / Lottery Ticket
 * Burst of confetti in crimson, gold, and cream on scratch reveal.
 */

import { useEffect, useRef } from "react";

const COLORS = [
  "#C9A84C", // aged gold
  "#F5D98B", // light gold
  "#8B1A1A", // deep crimson
  "#D4453A", // bright red
  "#FFF8E7", // cream
  "#E8C547", // yellow gold
  "#B22222", // firebrick
];

const SHAPES = ["square", "circle", "rect"] as const;

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  shape: (typeof SHAPES)[number];
  size: number;
  rotation: number;
  rotationSpeed: number;
  opacity: number;
  gravity: number;
}

export default function Confetti() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animFrameRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Spawn particles from center
    const cx = canvas.width / 2;
    const cy = canvas.height * 0.4;

    for (let i = 0; i < 180; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 4 + Math.random() * 12;
      particlesRef.current.push({
        x: cx + (Math.random() - 0.5) * 60,
        y: cy + (Math.random() - 0.5) * 30,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 6,
        color: COLORS[Math.floor(Math.random() * COLORS.length)],
        shape: SHAPES[Math.floor(Math.random() * SHAPES.length)],
        size: 6 + Math.random() * 8,
        rotation: Math.random() * Math.PI * 2,
        rotationSpeed: (Math.random() - 0.5) * 0.3,
        opacity: 1,
        gravity: 0.25 + Math.random() * 0.15,
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particlesRef.current = particlesRef.current.filter((p) => p.opacity > 0.01);

      for (const p of particlesRef.current) {
        ctx.save();
        ctx.globalAlpha = p.opacity;
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.fillStyle = p.color;

        if (p.shape === "square") {
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        } else if (p.shape === "circle") {
          ctx.beginPath();
          ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
          ctx.fill();
        } else {
          ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
        }

        ctx.restore();

        // Physics
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.vx *= 0.99;
        p.rotation += p.rotationSpeed;
        if (p.y > canvas.height * 0.7) {
          p.opacity -= 0.025;
        }
      }

      if (particlesRef.current.length > 0) {
        animFrameRef.current = requestAnimationFrame(draw);
      }
    };

    animFrameRef.current = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(animFrameRef.current);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 9999 }}
    />
  );
}
