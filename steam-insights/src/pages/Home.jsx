import { steamInsights } from "../projects/steamInsights";
import { shinyApp } from "../projects/shinyApp";

const projects = [steamInsights, shinyApp];

export default function Home() {
  return (
    <>
      {projects.map(p => (
        <ProjectSection key={p.id} project={p} />
      ))}
    </>
  );
}
