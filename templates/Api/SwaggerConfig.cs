using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.OpenApi.Models;
using System;

namespace {{ProjectNamespace}}.Api.Configurations
{
    public static class SwaggerConfig
    {
        public static void AddSwaggerConfiguration(this IServiceCollection services)
        {
            if (services == null) throw new ArgumentNullException(nameof(services));

            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new OpenApiInfo
                {
                    Version = "v1",
                    Title = "{{projectName}} API",
                    Description = "{{projectName}} API",
                    Contact = new OpenApiContact
                    {
                        Name = "{{author}}",
                        Email = "{{authorEmail}}",
                    }
                });

                c.CustomSchemaIds(type => type.ToString());
                c.SchemaFilter<SwaggerIgnoreFilter>();
            });
        }

        public static void UseSwaggerSetup(this IApplicationBuilder app)
        {
            if (app == null) throw new ArgumentNullException(nameof(app));

            app.UseSwagger();

            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("/swagger/v1/swagger.json", "{{projectName}} API");
            });
        }
    }
}
