import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about')({
  component: About,
})

function About() {
  return (
    <div className="p-2">
      <h3>About "The Architect's Ledger"</h3>
      <p>This application is designed to help authors follow the "Snowflake Method" for writing a novel, from a single sentence to a full manuscript.</p>
    </div>
  )
}
