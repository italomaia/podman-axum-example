# invoke tasks

from enum import Enum
from functools import reduce
from invoke import task
from invoke.context import Context
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Self
import os.path

PODMAN_BIN = "/usr/bin/podman"
COMPOSE_BIN = "/usr/bin/podman-compose"


class Env(Enum):
    DEV = 'dev'
    TST = 'tst'

    def __getitem__(self, name: str) -> Self:
        return super().__getitem__(name.upper()) # type: ignore

    def __str__(self):
        return self.name.lower()

    def envfile(self):
        return "envs/envfile-%s" % self

class ComposeCmd(Enum):
    UP = 'up'
    DOWN = 'down'
    STOP = 'stop'
    LOGS = 'logs'
    
    def __str__(self):
        return self.name.lower()

class Config:
    env: Env = Env.DEV

    def compose_files_arg(self, crate: Optional[str]=None) -> List[str]:
        file_list = ['docker-compose.yml']

        match self.env:
            case Env.DEV:
                file_list.extend(['docker-compose-dev.yml'])
            case Env.TST:
                file_list.extend(['docker-compose-dev.yml'])
                file_list.extend(['docker-compose-tst.yml'])
        
        if crate is not None:
            file_list = map(lambda v: os.path.join("infra/compose", crate, v), file_list)
        
        return list(reduce(lambda a, b: a+b, map(lambda v: ['-f', v], file_list)))


config = Config()

def build_compose_cmd(
        ctx: Context,
        command: ComposeCmd,
        crate: str,
        srv: Optional[str]=None,
        opts: Optional[str]=None,
    ):
    cmd = [COMPOSE_BIN] + config.compose_files_arg(crate) + [str(command)]

    if srv is not None:
        cmd += [srv]
    if opts is not None:
        cmd += [opts]

    ctx.run(' '.join(cmd))

# region: --- tasks

@task(name='env')
def task_env(ctx: Context, name: str):
    config.env = Env[name]

@task(name='up')
def task_up(ctx: Context, crate: str, srv: Optional[str]=None):
    build_compose_cmd(ctx, ComposeCmd.UP, crate, srv, '--detach')

@task(name='down')
def task_down(ctx: Context, crate: str, srv: Optional[str]=None):
    build_compose_cmd(ctx, ComposeCmd.DOWN, crate, srv)

@task(name='stop')
def task_stop(ctx: Context, crate: str, srv: Optional[str]=None):
    build_compose_cmd(ctx, ComposeCmd.STOP, crate, srv)

@task(name='logs')
def task_logs(ctx: Context, crate: str, srv: str, opts: Optional[str]=None):
    build_compose_cmd(ctx, ComposeCmd.LOGS, crate, srv, opts)

@task(name='img-build')
def img_build(
    ctx: Context,
    img: str,
    name: Optional[str]=None,
    repo: Optional[str]=None,
    tag: Optional[str]=None
):
    img_fpath = f"infra/images/Dockerfile.{img}"

    if not os.path.exists(img_fpath):
        print(f"Image file {img_fpath} could not be found")
        exit(1)
    
    build_args = []

    if name is None:
        name = img
    else:
        # if name is provided, we pass it as a build arg
        build_args += ["--build-arg", f"NAME={name}"]
    
    cmd = [PODMAN_BIN] + ["build", "-f", img_fpath, "-t", name]
    
    # images that build from source require a repo arg
    if repo:
        build_args += ["--build-arg", f"REPO={repo}"]

    # images that build from source require a tag arg
    if tag:
        build_args += ["--build-arg", f"TAG={tag}"]
    
    cmd += build_args

    print(cmd)

    ctx.run(' '.join(cmd))

# endregion: --- tasks
