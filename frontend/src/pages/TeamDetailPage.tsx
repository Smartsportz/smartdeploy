import { Link, useParams } from "react-router-dom";
import { Page } from "../components/UI";
import { teams } from "../data/platform";
import { InfoPanel, Metric, PageHero } from "./shared";

export function TeamDetailPage() {
  const { slug } = useParams();
  const team = teams.find((item) => item.slug === slug) ?? teams[0];

  return (
    <Page>
      <PageHero title={team.name} text="Team profile page for roster, approvals, documents, payment status, certificates, and tournament history." />
      <section className="detail-hero">
        <img src={team.image} alt="" />
        <div>
          <span className="status emerald">{team.rank}</span>
          <h1>{team.name}</h1>
          <p>{team.sport} team with {team.players} active players, performance rating {team.rating}, and {team.wins} recent wins.</p>
          <Link className="btn btn-primary" to="/user/registrations">Open registration</Link>
        </div>
      </section>
      <div className="detail-grid">
        <section className="panel">
          <h3>Team Metrics</h3>
          <div className="mini-grid">
            <Metric label="Players" value={`${team.players}`} />
            <Metric label="Wins" value={`${team.wins}`} />
            <Metric label="Rating" value={`${team.rating}`} />
          </div>
        </section>
        <InfoPanel title="Roster Controls" items={["Captain profile", "Player verification", "Document status", "Bench and substitutes"]} to="/admin/players" />
        <InfoPanel title="Tournament Links" items={["Approved entries", "Upcoming fixtures", "Live match history", "Certificates"]} to="/tournaments" highlight />
        <InfoPanel title="Payment Status" items={["Entry fee receipt", "Refund eligibility", "Invoice download", "Webhook audit"]} to="/user/payments" />
      </div>
    </Page>
  );
}
