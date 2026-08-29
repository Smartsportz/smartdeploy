import { Link, useParams } from "react-router-dom";
import { Page } from "../components/UI";
import { contentCards } from "../data/platform";
import { InfoPanel, PageHero } from "./shared";

export function ArticleDetailPage() {
  const { slug } = useParams();
  const article = contentCards.find((item) => item.slug === slug) ?? contentCards[0];
  const Icon = article.icon;

  return (
    <Page>
      <PageHero title={article.title} text="CMS-backed public content detail page connected from the blog and content containers." />
      <section className="panel article-page">
        <Icon size={30} />
        <span className="status emerald">{article.type}</span>
        <h2>{article.title}</h2>
        <p>Smart Sportz content pages support articles, galleries, FAQs, sponsor updates, operational guides, and SEO-ready CMS publishing.</p>
        <div className="hero-actions">
          <Link className="btn btn-primary" to="/blog">Back to blog</Link>
          <Link className="btn btn-secondary" to="/admin/cms/blogs">Edit in CMS</Link>
        </div>
      </section>
      <div className="detail-grid">
        <InfoPanel title="Content Workflow" items={["Draft content", "Attach media", "SEO review", "Publish to public website"]} to="/admin/cms/blogs" />
        <InfoPanel title="Audience Actions" items={["Read article", "Share update", "Open related tournament", "Contact organizer"]} to="/contact" highlight />
      </div>
    </Page>
  );
}
