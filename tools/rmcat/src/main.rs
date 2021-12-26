use std::{
    io::{ErrorKind, Read, Write},
    os::unix::prelude::AsRawFd,
    path::PathBuf,
};

use structopt::StructOpt;

#[derive(StructOpt)]
pub struct Options {
    file: PathBuf,
}

const BLOCK_SIZE: u64 = 4096 * 16;
const DEALLOC_SIZE: u64 = BLOCK_SIZE * 16;

fn main() -> std::io::Result<()> {
    let options = Options::from_args();

    let mut file = std::fs::OpenOptions::new().read(true).write(true).open(&options.file)?;
    std::fs::remove_file(&options.file)?;

    let mut buffer = [0; BLOCK_SIZE as usize];

    let mut deallocated = 0u64;
    let mut offset = 0u64;

    let stdout = std::io::stdout();
    let mut stdout = stdout.lock();

    loop {
        match file.read(&mut buffer) {
            Ok(0) => break,
            Ok(n) => {
                stdout.write_all(&buffer[..n])?;
                offset += n as u64;

                let dealloc_offset = offset / DEALLOC_SIZE;

                if dealloc_offset > deallocated {
                    let len = dealloc_offset - deallocated;
                    let res = unsafe {
                        libc::fallocate64(
                            file.as_raw_fd(),
                            libc::FALLOC_FL_PUNCH_HOLE | libc::FALLOC_FL_KEEP_SIZE,
                            (deallocated * DEALLOC_SIZE) as i64,
                            (len * DEALLOC_SIZE) as i64,
                        )
                    };
                    if res != 0 {
                        return Err(std::io::Error::last_os_error());
                    }
                    deallocated += len as u64;
                }
            }
            Err(err) if err.kind() == ErrorKind::Interrupted => continue,
            Err(err) => return Err(err),
        }
    }

    Ok(())
}
