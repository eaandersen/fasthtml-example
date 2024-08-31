from fasthtml.common import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta

# Set up the app with DaisyUI and Tailwind CSS
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app = FastHTML(hdrs=(tlink, dlink))

# Set up APScheduler
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler.start()

# Example job function
def print_job(job_type, message):
    print(f"{job_type} job executed at {datetime.now()}: {message}")

# Helper function to create a job card
def job_card(job):
    return Div(
        H3(job.name, cls="card-title"),
        P(f"Type: {job.trigger.__class__.__name__}"),
        P(f"Next run: {job.next_run_time}"),
        Button("Remove", hx_delete=f"/remove_job/{job.id}", hx_target="#job-list", cls="btn btn-error btn-sm"),
        cls="card bg-base-100 shadow-xl p-4 m-2"
    )

@app.get("/")
def home():
    jobs = scheduler.get_jobs()
    return Title("Job Scheduler"), Main(
        H1("Job Scheduler", cls="text-3xl font-bold mb-4"),
        Div(
            Form(
                hx_post="/add_job",
                hx_target="#job-list",
                cls="flex flex-col gap-2 mb-4"
            )(
                Input(name="job_name", placeholder="Job Name", cls="input input-bordered"),
                Input(name="job_message", placeholder="Job Message", cls="input input-bordered"),
                Select(name="job_type", cls="select select-bordered")(
                    Option("Single Use", value="single"),
                    Option("Interval", value="interval"),
                    Option("Cron", value="cron")
                ),
                Input(name="job_schedule", placeholder="Schedule (e.g., '5' for seconds, '*/5 * * * *' for cron)", cls="input input-bordered"),
                Button("Add Job", cls="btn btn-primary")
            ),
            Div(id="job-list", cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4")(
                *[job_card(job) for job in jobs]
            )
        ),
        cls="container mx-auto p-4"
    )

@app.post("/add_job")
def add_job(job_name: str, job_message: str, job_type: str, job_schedule: str):
    if job_type == "single":
        scheduler.add_job(print_job, 'date', run_date=datetime.now() + timedelta(seconds=int(job_schedule)), args=[job_type, job_message], id=job_name)
    elif job_type == "interval":
        scheduler.add_job(print_job, 'interval', seconds=int(job_schedule), args=[job_type, job_message], id=job_name)
    elif job_type == "cron":
        scheduler.add_job(print_job, 'cron', args=[job_type, job_message], id=job_name, **dict(zip(['minute', 'hour', 'day', 'month', 'day_of_week'], job_schedule.split())))
    
    return Div(*[job_card(job) for job in scheduler.get_jobs()])

@app.delete("/remove_job/{job_id}")
def remove_job(job_id: str):
    scheduler.remove_job(job_id)
    return Div(*[job_card(job) for job in scheduler.get_jobs()])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)