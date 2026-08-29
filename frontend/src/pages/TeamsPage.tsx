import { Page } from "../components/UI";
import { teams } from "../data/platform";
import { PageHero, TeamCard } from "./shared";

export function TeamsPage() {
  return (
    <Page>
      <PageHero title="Team Directory" text="Discover registered teams, rankings, rosters, and captain profiles." />
      <div className="team-grid">{teams.map((team) => <TeamCard key={team.name} team={team} />)}</div>
    </Page>
  );
}
