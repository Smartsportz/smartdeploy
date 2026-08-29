import { Page } from "../components/UI";
import { contentCards } from "../data/platform";
import { PageHero } from "./shared";
import { Link } from "react-router-dom";

export type ContentPageType = "gallery" | "blog" | "about" | "contact" | "sponsors" | "faq" | "leaderboards";

export function ContentPage({ type }: { type: ContentPageType }) {
  const titleMap = {
    gallery: "Media Gallery",
    blog: "Insights and News",
    about: "Our Story and Mission",
    contact: "Contact Center",
    sponsors: "Sponsorship Center",
    faq: "FAQ Center",
    leaderboards: "Professional Leaderboards",
  };

  return (
    <Page>
      <PageHero title={titleMap[type]} text="Premium content pages built into the public website structure with reusable CMS components." />
      <div className="content-grid">
        {contentCards.map((card) => {
          const Icon = card.icon;
          return (
            <Link className="click-card" to={card.path} key={card.title}>
            <article className="panel">
              <Icon size={24} />
              <span className="status emerald">{card.type}</span>
              <h3>{card.title}</h3>
              <p>Connected to the CMS API and optimized for the white default theme.</p>
            </article>
            </Link>
          );
        })}
      </div>
    </Page>
  );
}
