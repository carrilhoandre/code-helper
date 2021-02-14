using {{ProjectNamespace}}.Domain.Commands.Inputs.Projects;
using {{ProjectNamespace}}.Domain.Repositories;
using Microsoft.AspNetCore.Mvc;
using NetDevPack.Mediator;
using System.Threading.Tasks;

namespace {{ProjectNamespace}}.Api.Controllers
{
    [Route("api/[controller]")]
    public class {{className}}Controller : ApiController
    {
        [HttpPost("create")]
        public async Task<IActionResult> Post([FromBody] Create{{className}}Command command, 
                                              [FromServices]  IMediatorHandler _mediator)
        {
            return CustomResponse(await _mediator.SendCommand(command));
        }

        [HttpGet("list")]
        public async Task<IActionResult> List([FromServices] I{{className}}Repository _{{classNameLower}}Repository)
        {
            return CustomResponse(await _{{classNameLower}}Repository.List());
        }
    }
}
