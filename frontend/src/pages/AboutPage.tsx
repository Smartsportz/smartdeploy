import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Page } from "../components/UI";
import { Target, Eye, Users, Quote, Trophy } from "lucide-react";

export function AboutPage() {
  const fadeInUp = {
    hidden: { opacity: 0, y: 22 },
    visible: (customDelay: number = 0) => ({
      opacity: 1,
      y: 0,
      transition: { duration: 0.55, delay: customDelay, ease: [0.22, 1, 0.36, 1] },
    }),
  };

  const imageScale = {
    hidden: { opacity: 0, scale: 0.97 },
    visible: (customDelay: number = 0.15) => ({
      opacity: 1,
      scale: 1,
      transition: { duration: 0.65, delay: customDelay, ease: [0.22, 1, 0.36, 1] },
    }),
  };

  return (
    <Page className="about-page">
      {/* ==================================================
          1. HERO SECTION (Subtle Mint/Cream Background #f4f8f2)
      ================================================== */}
      <section className="about-hero-section">
        <div className="about-hero-container">
          <div className="about-hero-grid">
            <motion.div
              className="about-hero-text"
              initial="hidden"
              animate="visible"
              variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
            >
              <motion.span variants={fadeInUp} custom={0} className="about-eyebrow-text">
                ABOUT SMARTSPORTZ
              </motion.span>

              <motion.h1 variants={fadeInUp} custom={0.1} className="about-hero-title">
                About SmartSportz
              </motion.h1>

              <motion.p variants={fadeInUp} custom={0.2} className="about-hero-subtitle">
                Making Sport a Part of Everyday Life
              </motion.p>

              {/* Accent horizontal line under subtitle matching reference image */}
              <motion.div variants={fadeInUp} custom={0.25} className="about-hero-accent-line" />

              <motion.div variants={fadeInUp} custom={0.3} className="about-hero-paragraphs">
                <p>
                  Smartsportz was born with a simple idea: to bring people together through sport by creating sports events where everyone has a chance to play, compete, and find their tribe.
                </p>
                <p>
                  In a world where our days are increasingly spent at work desks, study tables, and in front of screens, we want to create opportunities for people to step away from their routines, get active, connect with others, and enjoy the sport they love.
                </p>
              </motion.div>

              <motion.div variants={fadeInUp} custom={0.4} className="about-hero-btn-wrap">
                <Link to="/tournaments" className="about-explore-btn">
                  Explore More
                </Link>
              </motion.div>
            </motion.div>

            <motion.div
              className="about-hero-media"
              initial="hidden"
              animate="visible"
              variants={imageScale}
              custom={0.2}
            >
              {/* Dot grid decoration: 5 columns x 8 rows between text and photo */}
              <div className="about-dot-grid" aria-hidden="true">
                {Array.from({ length: 40 }).map((_, i) => (
                  <span key={i} className="about-dot" />
                ))}
              </div>

              <div className="about-hero-image-frame">
                <img
                  src={`${import.meta.env.BASE_URL}assets/about/football-hero.png`}
                  alt="Young athletes competing in a football match organized by SmartSportz"
                  className="about-hero-football-img"
                  loading="eager"
                />
                <div className="about-floating-circle-badge" title="SmartSportz Community">
                  <Users size={24} />
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <div className="about-container">
        {/* ==================================================
            2. CRICKET & JOURNEY SECTION (White Background)
        ================================================== */}
        <section className="about-cricket-section">
          <motion.div
            className="about-cricket-grid"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={{ visible: { transition: { staggerChildren: 0.12 } } }}
          >
            <motion.div variants={imageScale} className="about-cricket-media">
              <div className="about-cricket-image-frame">
                <img
                  src={`${import.meta.env.BASE_URL}assets/about/team-huddle.png`}
                  alt="Cricket batsman playing a shot in an amateur community tournament"
                  className="about-cricket-img"
                  loading="lazy"
                />
                <div className="about-floating-community-card">
                  <div className="about-community-card-icon">
                    <Trophy size={18} />
                  </div>
                  <span>
                    Building Stronger<br />
                    Communities<br />
                    Through Sport
                  </span>
                </div>
              </div>
            </motion.div>

            <motion.div variants={fadeInUp} className="about-cricket-content">
              <div className="about-cricket-narrative-wrap">
                {/* Green vertical accent bar running down the narrative block */}
                <div className="about-cricket-vertical-bar" aria-hidden="true" />
                
                <div className="about-narrative-block">
                  <p>
                    Founded by a team of sports-loving people, Smartsportz is built around the belief that sport is more than professional competition. It is a way to stay active, build friendships, challenge yourself, have fun, and find an outlet from the pressures of everyday life.
                  </p>
                  <p>
                    Our journey begins in Bengaluru, India, with football as our first tournament. With badminton, chess, and several other sports in the pipeline, we are building tournaments and leagues for people across different age groups and skill levels.
                  </p>
                  <p className="about-transition-line">
                    But our ambition goes beyond conducting events.
                  </p>
                  <p>
                    We are building Smartsportz into a connected sports ecosystem where players and teams can create profiles, track performances, discover competitions, follow live scores, view statistics, and build their sporting journey through rankings and leagues.
                  </p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </section>

        {/* ==================================================
            3. OUR MISSION SECTION (Slanted Green Container Card)
        ================================================== */}
        <section className="about-mission-section">
          <motion.div
            className="about-mission-panel"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.25 }}
            variants={{ visible: { transition: { staggerChildren: 0.15 } } }}
          >
            <div className="about-mission-left">
              <motion.div variants={fadeInUp} className="about-circle-icon-badge">
                <Target size={22} />
              </motion.div>
              <motion.h2 variants={fadeInUp} className="about-panel-title">
                Our Mission
              </motion.h2>
              <motion.div variants={fadeInUp} className="about-panel-accent-line" />
              <motion.p variants={fadeInUp} className="about-panel-body">
                To make sport a part of everyday life by creating accessible, engaging, and competitive opportunities for everyone to play, compete, connect, and grow.
              </motion.p>
            </div>

            <motion.div variants={imageScale} className="about-mission-right">
              <div className="about-mission-img-wrap">
                <img
                  src={`${import.meta.env.BASE_URL}assets/about/badminton-match.png`}
                  alt="Badminton player lunging on court in competitive match"
                  className="about-mission-badminton-img"
                  loading="lazy"
                />
              </div>
            </motion.div>
          </motion.div>
        </section>

        {/* ==================================================
            4. OUR VISION SECTION (White Background)
        ================================================== */}
        <section className="about-vision-section">
          <motion.div
            className="about-vision-grid"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={{ visible: { transition: { staggerChildren: 0.15 } } }}
          >
            <motion.div variants={imageScale} className="about-vision-media">
              <div className="about-vision-image-frame">
                <img
                  src={`${import.meta.env.BASE_URL}assets/about/cricket-community.png `}
                  alt="Teammates stacking hands together in a celebratory team huddle"
                  className="about-vision-huddle-img"
                  loading="lazy"
                />
              </div>
            </motion.div>

            <motion.div variants={fadeInUp} className="about-vision-content">
              <div className="about-circle-icon-badge">
                <Eye size={22} />
              </div>
              <h2 className="about-section-heading">Our Vision</h2>
              <div className="about-accent-line" />

              <div className="about-narrative-block">
                <p>
                  To make sport the new social currency — where people choose a game over a drink, a team over a table, and shared experiences over sedentary routines.
                </p>
                <p>
                  We envision a culture where meeting friends doesn't always mean sitting around a table or heading to a bar. It means stepping onto a field, picking up a racket, sitting across a chessboard, competing together, laughing together, and building genuine connections through sport.
                </p>
                <p>
                  We want to make sport a primary socializing element in everyday life — bringing people together, creating communities, and making play a natural part of how we connect.
                </p>
              </div>
            </motion.div>
          </motion.div>
        </section>

        {/* ==================================================
            5. VISION HIGHLIGHT / QUOTE (Mint Green Card)
        ================================================== */}
        <section className="about-quote-section">
          <motion.div
            className="about-quote-panel"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.3 }}
            variants={fadeInUp}
          >
            <div className="about-quote-left">
              {/* Green vertical bar on the left */}
              <div className="about-quote-vertical-bar" aria-hidden="true" />
              
              {/* Green circle with white quote icon */}
              <div className="about-quote-icon-wrap">
                <Quote size={20} fill="currentColor" />
              </div>
              
              <div className="about-quote-text">
                <p>Starting from Bengaluru, growing across India, and eventually reaching the world.</p>
                <p>From a team of sports-loving people to a community of millions.</p>
              </div>
            </div>

            {/* Athlete silhouette graphic on the right */}
            <div className="about-quote-silhouette-wrap" aria-hidden="true">
              <img
                src={`${import.meta.env.BASE_URL}assets/about/quote-silhouettes.png`}
                alt="Athletes in motion silhouettes"
                className="about-quote-silhouette-img"
                loading="lazy"
              />
            </div>
          </motion.div>
        </section>

        {/* ==================================================
            6. CLOSING BRAND BANNER (Mint Green Card + Equipment)
        ================================================== */}
        <section className="about-closing-section">
          <motion.div
            className="about-closing-panel"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.25 }}
            variants={fadeInUp}
          >
            <div className="about-equipment-frame">
              <div className="about-closing-header">
                <h2 className="about-closing-main-title">SmartSportz —</h2>
                <p className="about-closing-tagline">Play. Compete. Connect. Grow.</p>
              </div>
              
              {/* Desktop Image (with text/layout configured for PC) */}
              <img
                src={`${import.meta.env.BASE_URL}assets/about/sports-equipment.png`}
                alt="Sports equipment"
                className="about-equipment-img desktop-img"
                loading="lazy"
              />

              {/* Mobile Image (clean background without text overlay issues) */}
              <img
                src={`${import.meta.env.BASE_URL}assets/about/sports-equipment-2.png`}
                alt="Sports equipment"
                className="about-equipment-img mobile-img"
                loading="lazy"
              />
            </div>
          </motion.div>
        </section>
      </div>
    </Page>
  );
}
