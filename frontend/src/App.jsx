import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Activity, LayoutDashboard, Users, HeartPulse, Brain, CalendarDays,
  FileBarChart, ShieldCheck, Settings, Search, Bell, ArrowUpRight,
  ArrowDownRight, ChevronDown, Menu, Download, Sparkles, Stethoscope,
  Clock3, CircleHelp, LogOut
} from "lucide-react";
import {
  AreaChart, Area, BarChart, Bar, CartesianGrid, XAxis, YAxis,
  Tooltip, ResponsiveContainer
} from "recharts";

const nav = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Patient analytics", icon: Users },
  { label: "Disease insights", icon: HeartPulse },
  { label: "AI predictions", icon: Brain },
  { label: "Appointments", icon: CalendarDays },
  { label: "Reports", icon: FileBarChart },
];
const secondary = [
  { label: "Security centre", icon: ShieldCheck },
  { label: "Settings", icon: Settings },
];
const trend = [
  { month: "Jan", patients: 82, visits: 58 },
  { month: "Feb", patients: 96, visits: 69 },
  { month: "Mar", patients: 91, visits: 65 },
  { month: "Apr", patients: 118, visits: 82 },
  { month: "May", patients: 109, visits: 78 },
  { month: "Jun", patients: 136, visits: 94 },
  { month: "Jul", patients: 128, visits: 89 },
  { month: "Aug", patients: 151, visits: 106 },
  { month: "Sep", patients: 143, visits: 99 },
  { month: "Oct", patients: 169, visits: 118 },
  { month: "Nov", patients: 158, visits: 111 },
  { month: "Dec", patients: 184, visits: 129 },
];
const departments = [
  { name: "Cardiology", count: 86, color: "#167D83" },
  { name: "Neurology", count: 64, color: "#40BFA5" },
  { name: "Endocrinology", count: 52, color: "#8C9FE8" },
  { name: "General care", count: 41, color: "#E7B66A" },
];
const kpis = [
  { label: "Total patients", value: "12,486", delta: "+8.2%", up: true, icon: Users, tone: "teal", note: "vs. previous period" },
  { label: "Appointments", value: "1,284", delta: "+4.6%", up: true, icon: CalendarDays, tone: "blue", note: "vs. previous period" },
  { label: "Active departments", value: "12", delta: "Stable", up: true, icon: Stethoscope, tone: "violet", note: "across the facility" },
  { label: "Reports generated", value: "394", delta: "+12.1%", up: true, icon: FileBarChart, tone: "amber", note: "vs. previous period" },
];

function Sidebar({ active, onSelect, open, onClose }) {
  return <><div className={`sidebar-backdrop ${open ? "show" : ""}`} onClick={onClose} />
    <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
      <div className="brand"><div className="brand-mark"><Activity size={21} strokeWidth={2.5}/></div><div><strong>healthpulse</strong><span>ANALYTICS PLATFORM</span></div></div>
      <div className="workspace"><div className="workspace-icon">HC</div><div><b>Healthcare Centre</b><small>Demo workspace</small></div><ChevronDown size={15}/></div>
      <div className="nav-caption">WORKSPACE</div>
      <nav>{nav.map(item => <button key={item.label} className={`nav-item ${active === item.label ? "active" : ""}`} onClick={() => { onSelect(item.label); onClose(); }}><item.icon size={18}/><span>{item.label}</span>{item.label === "AI predictions" && <i>3</i>}</button>)}</nav>
      <div className="nav-caption nav-caption-bottom">PREFERENCES</div>
      <nav>{secondary.map(item => <button key={item.label} className={`nav-item ${active === item.label ? "active" : ""}`} onClick={() => { onSelect(item.label); onClose(); }}><item.icon size={18}/><span>{item.label}</span></button>)}</nav>
      <div className="sidebar-bottom"><div className="support-card"><div className="support-icon"><CircleHelp size={17}/></div><b>Need a hand?</b><p>Explore the platform guide and learn how HealthPulse works.</p><button onClick={() => onSelect("Help & support")}>View help centre <ArrowUpRight size={14}/></button></div><div className="profile"><div className="avatar">AS</div><div><b>Admin Sample</b><small>Demo administrator</small></div><button aria-label="Profile menu"><ChevronDown size={16}/></button></div></div>
    </aside></>;
}

function KpiCard({ item, index }) {
  const Icon = item.icon;
  return <motion.article className="kpi-card" initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * .07, duration: .4 }}>
    <div className="kpi-top"><span>{item.label}</span><div className={`kpi-icon ${item.tone}`}><Icon size={18}/></div></div>
    <div className="kpi-value">{item.value}</div>
    <div className="kpi-foot"><span className={`delta ${item.up ? "positive" : "negative"}`}>{item.up ? <ArrowUpRight size={14}/> : <ArrowDownRight size={14}/>} {item.delta}</span><small>{item.note}</small></div>
  </motion.article>;
}

export default function App() {
  const [active, setActive] = useState("Overview");
  const [menuOpen, setMenuOpen] = useState(false);
  const [range, setRange] = useState("Last 12 months");
  const [query, setQuery] = useState("");
  const filteredDepartments = useMemo(() => departments.filter(d => d.name.toLowerCase().includes(query.toLowerCase())), [query]);

  return <div className="app-shell">
    <Sidebar active={active} onSelect={setActive} open={menuOpen} onClose={() => setMenuOpen(false)}/>
    <main className="main-area">
      <header className="topbar">
        <div className="topbar-left"><button className="icon-button mobile-menu" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu size={20}/></button><div className="breadcrumb">Workspace <span>/</span> <b>{active}</b></div></div>
        <div className="topbar-actions"><div className="searchbox"><Search size={16}/><input placeholder="Search anything..." aria-label="Search dashboard"/></div><button className="icon-button notification" aria-label="Notifications"><Bell size={18}/><i/></button><div className="topbar-divider"/><div className="top-user"><div className="avatar small">AS</div><span>Admin Sample</span><ChevronDown size={15}/></div></div>
      </header>
      <div className="page-content">
        <div className="welcome-row"><div><div className="eyebrow"><Sparkles size={14}/> HEALTHCARE INTELLIGENCE</div><h1>{active === "Overview" ? "Good morning, Admin" : active}</h1><p>Here’s what’s happening across your healthcare workspace.</p></div><div className="welcome-actions"><button className="btn-secondary"><Download size={16}/> Export report</button><button className="btn-primary"><Activity size={16}/> View analytics</button></div></div>
        <div className="demo-banner"><div className="demo-pulse"/><span><b>Demo environment</b> — All figures shown are illustrative sample data, not real patient or hospital records.</span><span className="demo-label">SAMPLE DATA</span></div>
        <section className="kpi-grid">{kpis.map((item, index) => <KpiCard key={item.label} item={item} index={index}/>)}</section>
        <section className="analytics-grid">
          <motion.article className="panel trend-panel" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .25 }}>
            <div className="panel-heading"><div><h2>Patient activity</h2><p>Registration and visit trends over time</p></div><select value={range} onChange={e => setRange(e.target.value)} aria-label="Select chart time range"><option>Last 12 months</option><option>Last 6 months</option><option>Last 30 days</option></select></div>
            <div className="chart-legend"><span><i className="legend-teal"/> Patient registrations</span><span><i className="legend-mint"/> Visits</span></div>
            <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><AreaChart data={range === "Last 6 months" ? trend.slice(-6) : trend} margin={{ top: 12, right: 8, left: -18, bottom: 0 }}><defs><linearGradient id="patientsFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#167D83" stopOpacity={.2}/><stop offset="95%" stopColor="#167D83" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#EDF1F5" vertical={false}/><XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: "#8793A3", fontSize: 11 }}/><YAxis axisLine={false} tickLine={false} tick={{ fill: "#8793A3", fontSize: 11 }}/><Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #E6EBF0", boxShadow: "0 8px 24px #101d3212" }}/><Area type="monotone" dataKey="patients" stroke="#167D83" strokeWidth={2.5} fill="url(#patientsFill)"/><Area type="monotone" dataKey="visits" stroke="#40BFA5" strokeWidth={2.5} fill="none"/></AreaChart></ResponsiveContainer></div>
          </motion.article>
          <motion.article className="panel department-panel" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .32 }}>
            <div className="panel-heading"><div><h2>Department activity</h2><p>Illustrative case distribution</p></div><button className="more-button" aria-label="More department options">•••</button></div>
            <label className="filter-input"><Search size={15}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Filter departments"/></label>
            <div className="department-list">{filteredDepartments.map((d, i) => <div className="department-row" key={d.name}><div className="department-meta"><span><i style={{ background: d.color }}/>{d.name}</span><b>{d.count}</b></div><div className="progress-track"><motion.div initial={{ width: 0 }} animate={{ width: `${d.count / 100 * 100}%` }} transition={{ duration: .7, delay: .35 + i * .08 }} style={{ background: d.color }}/></div></div>)}</div>
            <button className="text-link" onClick={() => setActive("Patient analytics")}>Explore department insights <ArrowUpRight size={15}/></button>
          </motion.article>
        </section>
        <section className="bottom-grid">
          <article className="panel insight-panel"><div className="insight-symbol"><Sparkles size={19}/></div><div><span className="eyebrow">INSIGHT SPOTLIGHT</span><h3>Make your data work harder</h3><p>Explore trends, compare model metrics, and turn structured datasets into clear, explainable insights.</p><button className="text-link" onClick={() => setActive("Disease insights")}>Explore insights <ArrowUpRight size={15}/></button></div></article>
          <article className="panel status-panel"><div className="panel-heading"><div><h2>Platform status</h2><p>Application environment</p></div><span className="status-chip"><i/> Demo ready</span></div><div className="status-line"><span><Activity size={16}/> Web interface</span><b>Available</b></div><div className="status-line"><span><ShieldCheck size={16}/> Security baseline</span><b>In development</b></div><div className="status-line"><span><Clock3 size={16}/> Last refreshed</span><b>Demo session</b></div></article>
        </section>
        <footer className="footer"><span>© 2026 HealthPulse Analytics</span><span>Built for learning, research and responsible data exploration.</span></footer>
      </div>
    </main>
  </div>;
}
