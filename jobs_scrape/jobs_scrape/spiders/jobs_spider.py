import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    job_skill = "Blockchain"
    job_location = "Boston US"

    def start_requests(self):
        yield scrapy.Request(
            f"https://stackoverflow.com/jobs?q={self.job_skill}&l={self.job_location}"
        )

    def parse(self, response):
        for link in response.css("a.s-link.stretched-link::attr(href)"):
            yield response.follow(
                f"https://stackoverflow.com" + link.get(),
                callback=self.parse_jobs,
            )

    def parse_jobs(self, response):
        yield {
            "Job Title": response.css("a.fc-black-900::attr(title)").get(),
            "Company": response.css("div.fc-black-700 a::text").get(),
            "Company logo image_url": response.css(
                "img.s-avatar--image::attr(src)"
            ).get(),
            "Location": response.css("div.fc-black-700 span::text")
            .get()
            .strip("\r\n                        –\r\n"),
            "Skills required": response.css(
                "div.d-flex.gs4.fw-wrap a::text"
            ).getall(),
            "Perks offered": response.css(
                "section.-benefits.mb32 ul li::attr(title)"
            ).getall(),
            "About this job": self.read_about_this_job(response),
            "Description": self.read_job_description(response),
            "Job link": f"https://stackoverflow.com"
            + response.css("a.fc-black-900::attr(href)").get(),
        }

    def read_about_this_job(self, response):
        about_this_job_elements = response.css("div.d-flex.gs16.gsx")
        about_this_job_contents = {}
        for about_job in about_this_job_elements.css("div.mb8"):
            key = about_job.css("span::text")[0].get()
            value = about_job.css("span::text")[1].get()
            about_this_job_contents[key] = value
        return about_this_job_contents

    def read_job_description(self, response):
        read_job_description_element = response.css(
            "section.mb32.fs-body2.fc-medium div"
        )
        read_job_description_content = read_job_description_element.css(
            "p::text"
        ).getall()

        return read_job_description_content
